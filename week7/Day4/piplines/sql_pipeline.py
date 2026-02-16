import sys
import os

# allow imports from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.schema_loader import SchemaLoader
from utils.query_validator import QueryValidator
from utils.safe_executor import SafeExecutor, ExecutionError
from utils.result_summarizer import ResultSummarizer
from generator.sql_generator import SQLGenerator

MAX_CORRECTION_ROUNDS = 2


class SQLPipeline:
    def __init__(self, db_config):
        self.schema_loader = SchemaLoader(db_config)
        self.generator = SQLGenerator()
        self.validator = QueryValidator(db_config)
        self.executor = SafeExecutor(db_config)
        self.summarizer = ResultSummarizer()

        # eagerly load schema so it's cached for all queries
        self._schema: dict | None = None
        self._schema_prompt: str | None = None

    # ── lazy schema init ────────────────────────────────────────────────
    def _ensure_schema(self):
        if self._schema_prompt is None:
            self._schema_prompt = self.schema_loader.schema_to_prompt()

    # ── main entry point ────────────────────────────────────────────────
    def ask(self, question: str) -> dict:
        self._ensure_schema()
        result = {
            "question": question,
            "sql": None,
            "validation": None,
            "result": None,
            "result_table": None,
            "summary": None,
            "error": None,
        }

        # ── Generate SQL ────────────────────────────────────────
        print(f"\nQuestion: {question}")
        gen = self.generator.generate(question, self._schema_prompt)
        sql = gen["sql"]
        result["sql"] = sql
        print(f"Generated SQL (attempt {gen['attempts']}):\n   {sql}\n")

        # ── Validate + self-correct loop ────────────────────
        for round_num in range(1, MAX_CORRECTION_ROUNDS + 1):
            validation = self.validator.validate(sql, explain_check=True)
            result["validation"] = validation

            if validation["valid"]:
                sql = validation["cleaned_query"]
                result["sql"] = sql
                print(f"Validation passed...")
                break

            print(
                f"Validation failed (round {round_num}): "
                f"{validation['errors']}"
            )

            if round_num < MAX_CORRECTION_ROUNDS:
                correction = self.generator.correct(
                    question, self._schema_prompt, sql, validation["errors"]
                )
                sql = correction["sql"]
                result["sql"] = sql
                print(f"Corrected SQL (attempt {correction['attempts']}):\n   {sql}\n")
        else:
            # all correction rounds exhausted
            if not result["validation"]["valid"]:
                result["error"] = (
                    "SQL could not be corrected after "
                    f"{MAX_CORRECTION_ROUNDS} attempts: "
                    + "; ".join(result["validation"]["errors"])
                )
                return result

        # ── Execute ─────────────────────────────────────────────
        try:
            exec_result = self.executor.execute(sql)
            result["result"] = exec_result
            table_text = SafeExecutor.to_text_table(exec_result)
            result["result_table"] = table_text
            print(f"Results ({exec_result['row_count']} rows):\n{table_text}\n")
        except ExecutionError as e:
            result["error"] = str(e)
            print(f"Execution error: {e}")
            return result

        # ── Step : Summarize ───────────────────────────────────────────
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
