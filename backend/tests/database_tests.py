"""
-setup for general test-driven development. incremental tests assure code has 100% coverage.
-for production systems database would be production server like Postgresql, etc. with mockups for test environments
-in this case we just re-use the "production" sqlite file

to run test suite, run `python -m pytest database_tests.py` in a terminal
"""

from pathlib import Path
from backend.create_database import Dbconnector
from backend.store import Task, Store

DB = Dbconnector()

# mocked tasks
task1 = Task("12346781326895423", "pomodoro project", "write a sample coding project",)
task2 = Task("778906475648709", "learn flask", "read all the books on flask")
task3 = Task("7579021236573678932", "teach python", "teach somebody how to use python")


class TestDatabaseFunctionality:
    def test_connection(self):
        result = DB.cursor.execute("""SELECT 1+1;""").fetchone()[0]
        assert result == 2

    def test_schema_load(self):
        tasks = DB.cursor.execute("""SELECT * FROM tasks;""").fetchone()
        tasklog = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchone()
        assert True  # will error if table doesn't exist

    def test_taskid_gets_entered_in_database(self):
        store = Store()
        store.add_task(task1)
        taskids = DB.cursor.execute("""SELECT * FROM tasks;""").fetchall()
        tasklogs = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchall()
        assert task1.id in [i[0] for i in taskids]
        assert task1.id in [i[0] for i in tasklogs]

    def test_tasks_default_to_unfinished(self):
        store = Store()
        task = task2
        store.add_task(task)
        finished = DB.cursor.execute(
            """SELECT done FROM tasklog WHERE taskid = ?""", [task.id]
        ).fetchone()[0]
        assert finished == 0

    def test_finishing_a_task(self):
        store = Store()
        task = task3
        store.add_task(task)
        store.finish_task(task.id)
        finished = DB.cursor.execute(
            """SELECT done FROM tasklog WHERE taskid = ?""", [task.id]
        ).fetchone()[0]
        assert finished == 1
