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

    ERROR(S):
    {errors}

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
        """
        Generate SQL for *question* given the schema context.

        Returns:
          {
            "sql": str,
            "attempts": int,
            "model": str,
          }
        """
        sql = self._call_llm(question, schema_prompt)
        return {
            "sql": sql,
            "attempts": 1,
            "model": MODEL,
        }

    # ── error-correction loop ───────────────────────────────────────────
    def correct(
        self,
        question: str,
        schema_prompt: str,
        bad_sql: str,
        errors: list[str],
    ) -> dict:
        attempts = 0
        current_errors = errors

        while attempts < MAX_CORRECTION_ATTEMPTS:
            attempts += 1
            corrected = self._call_correction(
                question, schema_prompt, current_errors
            )
            return {
                "sql": corrected,
                "attempts": attempts,
                "model": MODEL,
            }

        # exhausted attempts — return last attempt anyway
        return {
            "sql": bad_sql,
            "attempts": attempts,
            "model": MODEL,
        }

    # ── LLM interaction ─────────────────────────────────────────────────
    def _call_llm(self, question: str, schema_prompt: str) -> str:
        # replace {schema} in the system prompt with the actual schema context
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
        sqlQuery = response.choices[0].message.content.strip()
        return sqlQuery

    def _call_correction(
        self, question: str, schema_prompt: str, errors: list[str]
    ) -> str:
        prompt = CORRECTION_PROMPT.format(
            errors="\n".join(f"• {e}" for e in errors),
            question=question,
            schema=schema_prompt,
        )
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0,
        )
        sql = response.choices[0].message.content.strip()
        return sql


