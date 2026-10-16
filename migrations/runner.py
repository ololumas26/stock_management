import importlib
from pathlib import Path



files_pattern = '[0-9][0-9][0-9]_*.py'

def run_migrations(connection, migrations_path="migrations"):

    connection.execute("""

    CREATE TABLE IF NOT EXISTS schema_migrations(
        version INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")

    versions = {
        row[0]
        for row in connection.execute(
            "SELECT version FROM schema_migrations"
        )
    }

    files = sorted(Path(migrations_path).glob(files_pattern))


    for file in files:
        version = int(file.name[:3])

        if version in versions:
            continue

        module_name = f"migrations.{file.stem}"
        migration = importlib.import_module(module_name)

        try:
            connection.execute("BEGIN")
            migration.upgrade(connection)
            connection.execute("""
                INSERT INTO schema_migrations(version, name) VALUES (?, ?)
                    """,(version, file.name))

            connection.commit()

        except Exception:
            connection.rollback()
            raise


# Compatibilidade com o nome usado anteriormente no main.py.
run_migration = run_migrations

