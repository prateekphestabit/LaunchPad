import psycopg2
import psycopg2.extras
import os
from typing import Optional


DEFAULT_ROW_LIMIT = 500
DEFAULT_TIMEOUT_MS = 10_000  # 10 s


class ExecutionError(Exception):
    """Raised when query execution fails."""
    pass


class SafeExecutor:
    def __init__(self, db_config, row_limit = DEFAULT_ROW_LIMIT, timeout_ms = DEFAULT_TIMEOUT_MS,):
        self.db_config = db_config
        self.row_limit = row_limit
        self.timeout_ms = timeout_ms

    def execute(self, query: str) -> dict:
        conn = psycopg2.connect(**self.db_config)
        try:
            conn.set_session(readonly=True, autocommit=False)

            cur =  conn.cursor()
            # ── guardrails ──────────────────────────────────────────
            cur.execute(f"SET statement_timeout = {self.timeout_ms};")
            cur.execute(query)

            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = cur.fetchall()

            truncated = len(rows) > self.row_limit
            if truncated:
                rows = rows[: self.row_limit]

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "truncated": truncated,
            }
        except psycopg2.Error as e:
            raise ExecutionError(f"Query execution failed: {e}") from e
        finally:
            conn.rollback()
            conn.close()

    # ── convenience: pretty text table ──────────────────────────────────
    @staticmethod
    def to_text_table(result: dict) -> str:
        """Render the result dict as a plain-text table."""
        if not result["columns"]:
            return "(no results)"

        cols = result["columns"]
        rows = result["rows"]

        # compute column widths
        widths = [len(c) for c in cols]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))

        def fmt_row(values):
            return " | ".join(str(v).ljust(w) for v, w in zip(values, widths))

        header = fmt_row(cols)
        sep = "-+-".join("-" * w for w in widths)
        body = "\n".join(fmt_row(r) for r in rows)

        table = f"{header}\n{sep}\n{body}"
        if result["truncated"]:
            table += f"\n… (results truncated to {result['row_count']} rows)"
        return table
