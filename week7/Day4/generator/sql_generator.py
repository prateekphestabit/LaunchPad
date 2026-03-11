import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

MAX_CORRECTION_ATTEMPTS = 2

# ──────────────────────────── system prompt ──────────────────────────────
SQL_SYSTEM_PROMPT = """You are an expert SQL assistant for PostgreSQL.
    RULES
    1. Output ONLY the SQL query — no explanations, no markdown fences.
    2. Use ONLY tables and columns present in the schema below.
    3. Always qualify ambiguous columns with their table name.
    4. Use standard PostgreSQL syntax; never use non-standard functions.
    5. Prefer explicit JOINs over implicit comma joins.
    6. For date filtering use standard comparisons (e.g., EXTRACT(YEAR FROM col) = 2023).
    7. Never use DROP, DELETE, INSERT, UPDATE, ALTER, TRUNCATE, or any DDL/DML
    that modifies data.
    8. Always return a SELECT statement.
    9. Some Times questions may contain names of artists so user can make spelling mistakes. In that case, try to infer the correct name based on the schema and answer the question accordingly.
    
    DATABASE SCHEMA
    {schema}
"""

CORRECTION_PROMPT = """The SQL you generated is invalid.
    INVALID SQL: {bad_sql}

    ERROR(S): {errors}

    BLOCKED KEYWORDS: [ "DROP", "DELETE", "TRUNCATE",
    "ALTER", "INSERT", "UPDATE", "CREATE", "GRANT",
    "REVOKE", "EXEC", "EXECUTE", "COPY", "\\copy",]
    
    ORIGINAL QUESTION: {question}

    DATABASE SCHEMA:
    {schema}

    Please output ONLY the corrected SQL query (no explanations, no markdown).
"""


class SQLGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    # ── main entry ──────────────────────────────────────────────────────
    def generate(self, question: str, schema_prompt: str) -> dict:
        sql = self._call_llm(question, schema_prompt)
        return sql

    # ── error-correction loop ───────────────────────────────────────────
    def correct(self, question, schema_prompt, bad_sql, errors):
        corrected = self._call_correction(question, schema_prompt, bad_sql, errors)
        return corrected

    # ── LLM interaction ─────────────────────────────────────────────────
    def _call_llm(self, question: str, schema_prompt: str) -> str:
        system = SQL_SYSTEM_PROMPT.format(schema=schema_prompt) 
        
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
            max_tokens=1024,
            temperature=0,
        )
        sqlQuery = response.choices[-1].message.content.strip()
        return sqlQuery

    def _call_correction(self, question, schema_prompt, bad_sql, errors):
        prompt = CORRECTION_PROMPT.format(
            errors=errors,
            question=question,
            schema=schema_prompt,
            bad_sql=bad_sql,
        )
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0,
        )
        sql = response.choices[-1].message.content.strip()
        return sql


