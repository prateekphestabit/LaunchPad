import os
from typing import Optional
from groq import Groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")


SUMMARIZE_SYSTEM = """
    You are a data analyst assistant. You MUST answer the user's
    question by referencing the ACTUAL data from the result table provided.

    STRICT RULES:
    1. Use the EXACT numbers and values from the result table — never make up data.
    2. Mention specific rows, names, and figures from the results (e.g. "Drake had $6,375.59 in sales").
    3. Identify the highest, lowest, and any notable patterns IN the data.
    4. If the table has a ranking or ordering, explain it clearly.
    5. If the table is empty, say "The query returned no results."
    6. Keep it under 200 words.
    7. Format currency values with $ and commas.
    8. Do NOT say generic things like "the data provides insight" — be specific.
"""


class ResultSummarizer:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = MODEL
        self.client = Groq(api_key=self.api_key)

    def summarize(self, question ,sql_query ,result_table ,row_count ,truncated):
        user_content = (
            f"Answer this question using ONLY the data below.\n\n"
            f"**Question:** {question}\n\n"
            f"**SQL query that was run:**\n```sql\n{sql_query}\n```\n\n"
            f"**Query results ({row_count} rows"
            f"{', truncated' if truncated else ''}):**\n```\n{result_table}\n```\n\n"
            f"Now summarize these results. Reference the actual values from the table above."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SUMMARIZE_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=512,
            temperature=0.3,
        )

        return response.choices[-1].message.content.strip()
