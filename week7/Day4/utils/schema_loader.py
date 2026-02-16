import psycopg2

class SchemaLoader:
    def __init__(self, db_config):
        self.db_config = db_config

    # ── pretty-print for LLM prompt context ─────────────────────────────
    def schema_to_prompt(self, schema="public"):
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        # ---- 1. Get columns ----
        cur.execute("""
            SELECT table_name,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
            FROM information_schema.columns
            WHERE table_schema = %s
            ORDER BY table_name, ordinal_position;
        """, (schema,))
        columns = cur.fetchall()

        # ---- 2. Get primary keys ----
        cur.execute("""
            SELECT tc.table_name, kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = %s;
        """, (schema,))
        pk_rows = cur.fetchall()
        primary_keys = {(t, c) for t, c in pk_rows}

        # ---- 3. Get foreign keys ----
        cur.execute("""
            SELECT tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table,
                    ccu.column_name AS foreign_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = %s;
        """, (schema,))
        fk_rows = cur.fetchall()

        # Organize foreign keys
        foreign_keys = {}
        for table, column, ref_table, ref_column in fk_rows:
            foreign_keys[(table, column)] = (ref_table, ref_column)

        # Organize columns by table
        schema_dict = {}
        for table, column, dtype, nullable, default in columns:
            schema_dict.setdefault(table, []).append(
                (column, dtype, nullable, default)
            )

        # ---- Build output ----
        output = []

        for table, cols in schema_dict.items():
            lines = []

            for column, dtype, nullable, default in cols:
                col_def = f"{column} {dtype.upper()}"

                if (table, column) in primary_keys:
                    col_def += " PRIMARY KEY"

                if nullable == "NO":
                    col_def += " NOT NULL"

                if (table, column) in foreign_keys:
                    ref_table, ref_column = foreign_keys[(table, column)]
                    col_def += f" REFERENCES {ref_table}({ref_column})"

                lines.append(col_def)

            table_block = f"{table}(\n  " + ",\n  ".join(lines) + "\n)"
            output.append(table_block)

        conn.close()
        return "\n\n".join(output)



