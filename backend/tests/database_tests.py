"""
-setup for general test-driven development. incremental tests assure code has 100% coverage.
-for production systems database would be production server like Postgresql, etc. with mockups for test environments
-in this case we just re-use the "production" sqlite file

run test suite `python -m pytest database_tests.py`
"""

from pathlib import Path
from backend.create_database import Dbconnector
from backend.store import Task, Store

DB = Dbconnector()


class TestDatabaseFunctionality:
    def test_connection(self):
        result = DB.cursor.execute("""SELECT 1+1;""").fetchone()[0]
        assert result == 2

    def test_schema_load(self):
        tasks = DB.cursor.execute("""SELECT * FROM tasks;""").fetchone()
        tasklog = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchone()
        assert True  # will error if table doesn't exist

    def test_taskid_gets_entered_in_database(self):
        sample_taskid = "aiuopqewr1234"
        sample_task = Task(
            sample_taskid,
            "pomodoro project",
            "write a sample coding project to create a pomodoro timer",
        )
        store = Store()
        store.add_task(sample_task)
        taskids = DB.cursor.execute("""SELECT * FROM tasks;""").fetchall()
        tasklogs = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchall()
        assert sample_taskid in [i[0] for i in taskids]
        assert sample_taskid in [i[0] for i in tasklogs]
