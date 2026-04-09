def validate_sql(sql):
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT"]

    for word in forbidden:
        if word in sql.upper():
            raise Exception("Unsafe query detected")

    return sql