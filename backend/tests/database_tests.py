"""
setup for general test-driven development. incremental tests assure code has 100% coverage.
run test suite `python -m pytest database_tests.py`
"""

from pathlib import Path
from backend.create_database import Dbconnector

DATABASE = Path("../pomodoro.db")
DB = Dbconnector(DATABASE)


class TestDatabaseFunctionality:
    def test_connection(self):
        result = DB.cursor.execute("""SELECT 1+1;""").fetchone()[0]
        assert result == 2

    def test_schema_load(self):
        tasks = DB.cursor.execute("""SELECT * FROM tasks;""").fetchone()
        tasklog = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchone()
        assert True  # will error if table doesn't exist

    def test_insert_data(self):
        # will not continue TDD for the rest of the database
        pass
