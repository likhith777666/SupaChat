def format_response(rows):
    if not rows:
        return {
            "summary": "No data found",
            "data": []
        }

    summary = f"Returned {len(rows)} rows"

    return {
        "summary": summary,
        "data": rows
    }