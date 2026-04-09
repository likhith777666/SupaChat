# mcp_translator.py

# from openai import OpenAI
import json
import os
import requests
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your DB schema (VERY IMPORTANT)
SCHEMA = """
Table: posts
Columns:
- id (integer)
- title (text)
- topic (text)
- views (integer)
- likes (integer)
- created_at (date)
"""

# 🔥 Strong system prompt (forces JSON)
SYSTEM_PROMPT = f"""
You are an MCP (Model Context Protocol) query translator.

Convert user query into STRICT JSON.

Schema:
{SCHEMA}

Rules:
- Output ONLY valid JSON
- No explanation
- No markdown
- No comments
- Always include:
  - action
  - filters
  - sort_by (optional)
  - order (optional)
  - limit (optional)

Examples:

User: show top 3 AI posts
Output:
{{
  "action": "query_posts",
  "filters": {{"topic": "AI"}},
  "sort_by": "views",
  "order": "desc",
  "limit": 3
}}

User: list all frontend posts
Output:
{{
  "action": "query_posts",
  "filters": {{"topic": "Frontend"}}
}}
"""

def extract_json(text: str):
    try:
        # 1. Try markdown ```json ... ```
        match = re.search(r"```json(.*?)```", text, re.DOTALL)

        if match:
            json_str = match.group(1)
        else:
            # 2. Try first {...}
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                json_str = match.group(0)
            else:
                raise ValueError("No JSON found in response")

        # 3. Remove comments (// ...)
        json_str = re.sub(r"//.*", "", json_str)

        # 4. Remove trailing commas (common LLM mistake)
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)

        return json.loads(json_str)

    except Exception as e:
        return {
            "action": "error",
            "error": f"JSON parsing failed: {str(e)}",
            "raw": text
        }


def translate_query(user_query: str):
    api_key = os.getenv("GROQ_API_KEY")
    try:
        print("this is translate_query function")  # Debug log
        response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        }
    )
        # 🔥 Step 1: Raw response
        print("MCP Translation API Response:", response.text)

        # 🔥 Step 2: Convert to dict
        data = response.json()

        print("Parsed response dict:", data)

        # 🔥 Step 3: Extract content
        content = data["choices"][0]["message"]["content"]

        print("🔍 Raw LLM Content:\n", content)

        # 🔥 Step 4: Parse JSON (since your output is clean)
        parsed = json.loads(content)

        print("✅ Parsed MCP:\n", parsed)

        return parsed

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "action": "error",
            "error": str(e),
            "raw": user_query
        }