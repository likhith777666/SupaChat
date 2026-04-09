# import requests
# import os

# def generate_sql(query):
#     response = requests.post(
#         "https://api.openai.com/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
#         },
#         json={
#             "model": "gpt-4o-mini",
#             "messages": [
#                 {
#                     "role": "system",
#                     "content": "Convert user query into SQL. Only return SQL. Table: articles(id,title,topic,views,likes,created_at)"
#                 },
#                 {
#                     "role": "user",
#                     "content": query
#                 }
#             ]
#         }
#     )

#     return response.json()["choices"][0]["message"]["content"]


import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_sql(query):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not found in .env")

    print("Using API Key:", api_key[:5], "****")  # safe debug

    # Debug check
    # print("Groq API Key:", api_key)

    if not api_key:
        raise Exception("GROQ_API_KEY is not set in environment variables")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a PostgreSQL SQL generator.STRICT RULES:1. Only use this table:   articles(id, title, topic, views, likes, created_at)2. Do NOT use any other table names.3. Do NOT use columns that are not listed above.4. Return ONLY SQL query (no explanation, no markdown).5. Do NOT use ```sql or backticks.6. Always generate valid PostgreSQL syntax. No explanation."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    # Debug response
    print("AI Response:", response.text)

    result = response.json()

    # ✅ Extract SQL safely
    sql = result["choices"][0]["message"]["content"]

    # ✅ Clean formatting (important)
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print("Generated SQL:", sql)

    return sql