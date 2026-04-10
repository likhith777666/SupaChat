from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection
from ai import generate_sql
from mcp import validate_sql
from formatter import format_response
from fastapi.middleware.cors import CORSMiddleware
from mcptranslator import translate_query
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)
class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "okkk"}

@app.post("/query")
def query_data(req: QueryRequest):
    try:
        mcp = translate_query(req.query)
        print("MCP Output:", mcp)

        # 🔥 STEP 2: Decide SQL source
        if mcp.get("action") == "query_posts":
            sql = build_sql_from_mcp(mcp)
        else:
            print("⚠️ Falling back to AI SQL generation")
            sql = generate_sql(user_query)
        # Step 1: NL → SQL
        sql = generate_sql(req.query)
 
        # Step 2: Validate
        safe_sql = validate_sql(sql)

        # Step 3: Execute
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(safe_sql)

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        conn.close()

        # Step 4: Format
        response = format_response(result)

        return {
            "sql": safe_sql,
            **response
        }

    except Exception as e:
        return {"error": str(e)}
    
def build_sql_from_mcp(mcp: dict):
    base_query = "SELECT * FROM posts"
    conditions = []

    filters = mcp.get("filters", {})

    # 🔹 Dynamic filters
    for key, value in filters.items():
        if isinstance(value, str):
            conditions.append(f"{key} = '{value}'")
        else:
            conditions.append(f"{key} = {value}")

    # WHERE clause
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # 🔹 Sorting
    if mcp.get("sort_by"):
        order = mcp.get("order", "desc").upper()
        base_query += f" ORDER BY {mcp['sort_by']} {order}"

    # 🔹 Limit
    if mcp.get("limit"):
        base_query += f" LIMIT {mcp['limit']}"

    return base_query + ";"