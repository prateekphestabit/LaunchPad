"""
Query Validator — Validates and sanitises generated SQL.

Three layers of safety:
  1. Structural parse via sqlparse (syntax check)
  2. Blocklist of forbidden statements (DROP, DELETE, ALTER …)
  3. Optional EXPLAIN-based validation against the live database
"""

import re
import sqlparse
from sqlparse.sql import Statement
from typing import Optional
import psycopg2
import os


# ── statements the validator will REJECT ────────────────────────────────
BLOCKED_KEYWORDS = {
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
}

class QueryValidator:
    def __init__(self, db_config):
        self.db_config = db_config

    # ── public entry point ──────────────────────────────────────────────
    def validate(self, sqlQuery, explain_check: bool = True) -> dict:
        errors: list[str] = []

        # 1. structural / syntax
        syntax_ok, syntax_err = self._check_syntax(sqlQuery)
        if not syntax_ok:
            errors.append(f"Syntax error: {syntax_err}")

        # 2. blocklist
        blocked = self._check_blocklist(sqlQuery)
        if blocked:
            errors.append(f"Blocked keyword(s) detected: {', '.join(blocked)}")

        # 3. injection patterns
        injection = self._check_injection_patterns(sqlQuery)
        if injection:
            errors.append(f"Possible SQL injection pattern: {injection}")

        # 4. EXPLAIN validation (only if no prior errors)
        if not errors and explain_check:
            explain_ok, explain_err = self._explain_check(sqlQuery)
            if not explain_ok:
                errors.append(f"EXPLAIN failed: {explain_err}")

        return {
            "valid": len(errors) == 0,
            "cleaned_query": sqlQuery,
            "errors": errors,
        }

    # ── internal checks ─────────────────────────────────────────────────

    def _check_syntax(self, query: str) -> tuple[bool, Optional[str]]:
        try:
            parsed = sqlparse.parse(query)
            if not parsed or not str(parsed[0]).strip():
                return False, "Empty or unparseable query"
            return True, None
        except Exception as e:
            return False, str(e)

    def _check_blocklist(self, query: str) -> list[str]:
        tokens = set(
            t.ttype is not None and t.normalized
            for stmt in sqlparse.parse(query)
            for t in stmt.flatten()
        )
        # simple upper-case word scan as fallback
        words = set(re.findall(r"\b[A-Z_]+\b", query.upper()))
        found = words & BLOCKED_KEYWORDS
        return sorted(found)

    def _check_injection_patterns(self, query: str) -> Optional[str]:
        patterns = [
            (r";\s*(DROP|DELETE|ALTER|INSERT|UPDATE)\b", "chained destructive statement"),
            (r"'\s*OR\s+'1'\s*=\s*'1'", "tautology injection"),
            (r"UNION\s+ALL\s+SELECT", "UNION injection"),
            (r"--\s*$", "comment termination"),
        ]
        for pat, desc in patterns:
            if re.search(pat, query, re.IGNORECASE):
                return desc
        return None

    def _explain_check(self, query: str) -> tuple[bool, Optional[str]]:
        """Run EXPLAIN on the query to let PostgreSQL validate it."""
        try:
            conn = psycopg2.connect(**self.db_config)
            try:
                with conn.cursor() as cur:
                    cur.execute(f"EXPLAIN {query}")
                return True, None
            finally:
                conn.rollback()
                conn.close()
        except psycopg2.Error as e:
            return False, str(e).strip()
        except Exception as e:
            return False, str(e).strip()
