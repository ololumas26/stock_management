import sqlite3
import unittest

from migrations.runner import run_migrations


class TestDatabaseMigrations(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:", isolation_level=None)
        self.connection.execute("PRAGMA foreign_keys = ON")

    def tearDown(self):
        self.connection.close()

    def test_run_migrations_creates_schema(self):
        run_migrations(self.connection)

        tables = {
            row[0]
            for row in self.connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            )
        }

        self.assertTrue({
            "schema_migrations",
            "products",
            "stocks",
            "movements",
        }.issubset(tables))

    def test_run_migrations_is_idempotent(self):
        run_migrations(self.connection)
        run_migrations(self.connection)

        applied = self.connection.execute(
            "SELECT version, name FROM schema_migrations"
        ).fetchall()

        self.assertEqual(applied, [(1, "001_initial_tables.py")])


if __name__ == "__main__":
    unittest.main()
