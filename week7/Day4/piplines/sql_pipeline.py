import sys
import os

# allow imports from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.query_validator import QueryValidator
from utils.safe_executor import SafeExecutor
from utils.result_summarizer import ResultSummarizer
from generator.sql_generator import SQLGenerator

MAX_CORRECTION_ROUNDS = 2

schema = '''
albums(
  album_id INTEGER PRIMARY KEY NOT NULL,
  title CHARACTER VARYING NOT NULL,
  artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
  release_date DATE,
  price NUMERIC
)

artists(
  artist_id INTEGER PRIMARY KEY NOT NULL,
  name CHARACTER VARYING NOT NULL,
  genre CHARACTER VARYING,
  country CHARACTER VARYING
)

sales(
  sale_id INTEGER PRIMARY KEY NOT NULL,
  album_id INTEGER NOT NULL REFERENCES albums(album_id),
  sale_date DATE NOT NULL,
  quantity INTEGER NOT NULL,
  total_amount NUMERIC NOT NULL
)
'''

class SQLPipeline:
    def __init__(self, db_config):
        self.generator = SQLGenerator()
        self.validator = QueryValidator()
        self.executor = SafeExecutor(db_config)
        self.summarizer = ResultSummarizer()

    # ── main entry point ────────────────────────────────────────────────
    def ask(self, question: str) -> dict:
        result = {
            "question": question,
            "sql": None,
            "validation": None,
            "result": None,
            "result_table": None,
            "summary": None,
            "error": None,
        }

        # ── Step 1: Generate SQL ────────────────────────────────────────
        print(f"\nQuestion: {question}")
        sql = self.generator.generate(question, schema)
        result["sql"] = sql
        print(f"Generated SQL (attempt 1):\n   {sql}\n")

        # ── Step 2: Validate + self-correct loop ────────────────────
        for round_num in range(1, MAX_CORRECTION_ROUNDS + 1):
            validation = self.validator.validate(sql)
            result["validation"] = validation

            if validation:
                print(f"Validation passed...")
                break

            print(f"Validation failed (round {round_num})")

            if round_num < MAX_CORRECTION_ROUNDS:
                sql = self.generator.correct(
                    question,
                    schema,
                    sql, 
                    "there was either a syntax error or blocked keywords in the SQL. Please fix it."
                )
                result["sql"] = sql
                print(f"Corrected SQL (attempt {round_num}):\n   {sql}\n")
            
        if not result["validation"]:
            result["error"] = (
                "SQL could not be corrected after "
                f"{MAX_CORRECTION_ROUNDS} attempts: "
            )
            return result

        # ── Step 3: Execute ─────────────────────────────────────────────
        
        exec_result = self.executor.execute(sql)
        result["result"] = exec_result
        table_text = SafeExecutor.to_text_table(exec_result)
        result["result_table"] = table_text
        print(f"Results ({exec_result['row_count']} rows):\n{table_text}\n")
    

        # ── Step 4: Summarize ───────────────────────────────────────────
        try:
            summary = self.summarizer.summarize(
                question=question,
                sql_query=sql,
                result_table=table_text,
                row_count=exec_result["row_count"],
                truncated=exec_result["truncated"],
            )
            result["summary"] = summary
            print(f"Summary:\n{summary}\n")
        except Exception as e:
            result["error"] = f"Summarization failed: {e}"
            print(f"Summarization error: {e}")

        return result
