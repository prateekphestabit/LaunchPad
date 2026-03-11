import sqlparse

# ── statements the validator will REJECT ────────────────────────────────
BLOCKED_KEYWORDS = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "INSERT",
    "UPDATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "COPY",
    "\\copy",
]

class QueryValidator:
    def validate(self, sqlQuery):

        # 1. syntax check
        parsed = sqlparse.parse(sqlQuery)
        if not parsed or not str(parsed[0]).strip():
            return False
            
        # 2. blocklist
        for word in BLOCKED_KEYWORDS:
            if word in sqlQuery.upper():
                return False

        return True
