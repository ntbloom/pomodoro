"""
-setup for general test-driven development. incremental tests assure code has 100% coverage.
-for production systems database would be production server like Postgresql, etc. with mockups for test environments
-in this case we just re-use the "production" sqlite file

to run test suite, run `python -m pytest database_tests.py` in a terminal
"""


from datastore.create_database import Dbconnector
from datastore.store import Task, Store
import pytest
import requests
from flask import jsonify
from pathlib import Path
import os

filename = Path("../test_database.db")
DATABASE = os.path.abspath(filename)
DB = Dbconnector(DATABASE)
localhost = "http://127.0.0.1:5000"

# mocked tasks -- in production would use either greater qty of tasks or use property-based testing
task1 = Task("12346781326895423", "pomodoro project", "write a sample coding project",)
task2 = Task("778906475648709", "learn flask", "read all the books on flask")
task3 = Task("7579021236573678932", "teach python", "teach somebody how to use python")


class TestStoreClass:
    @pytest.fixture(scope="function", autouse=True)
    def make_clean_database_each_time(self):
        DB.load_schema()
        yield

    def test_connection(self):
        result = DB.cursor.execute("""SELECT 1+1;""").fetchone()[0]
        assert result == 2

    def test_schema_load(self):
        tasks = DB.cursor.execute("""SELECT * FROM tasks;""").fetchone()
        tasklog = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchone()
        assert True  # will error if table doesn't exist

    def test_taskid_gets_entered_in_database(self):
        store = Store(DATABASE)
        store.add_task(task1)
        taskids = DB.cursor.execute("""SELECT * FROM tasks;""").fetchall()
        tasklogs = DB.cursor.execute("""SELECT * FROM tasklog;""").fetchall()
        # DB.commit()
        assert task1.id in [i[0] for i in taskids]
        assert task1.id in [i[0] for i in tasklogs]

    def test_tasks_default_to_unfinished(self):
        store = Store(DATABASE)
        task = task2
        store.add_task(task)
        finished = DB.cursor.execute(
            """SELECT done FROM tasklog WHERE taskid = ?""", [task.id]
        ).fetchone()[0]
        assert finished == 0

    def test_finishing_a_task(self):
        store = Store(DATABASE)
        task = task3
        store.add_task(task)
        store.mark_task_as_finished(task.id)
        finished = DB.cursor.execute(
            """SELECT done FROM tasklog WHERE taskid = ?""", [task.id]
        ).fetchone()[0]
        assert finished == 1

    def test_make_dict(self):
        store = Store(DATABASE)
        task = task1
        new_dict = {
            "taskid": task.id,
            "short": task.short,
            "desc": task.desc,
            "done": task.done,
        }
        assert store.make_dict(task) == new_dict

    def test_get_all_tasks(self):
        store = Store(DATABASE)
        test_tasks = [task1, task2, task3]
        for i in test_tasks:
            store.add_task(i)
        expected_tasks = [store.make_dict(i) for i in test_tasks]
        actual_tasks = store.get_all_tasks()
        assert actual_tasks == expected_tasks

    def test_get_task_info(self):
        store = Store(DATABASE)
        tasks = [task1, task2, task3]
        for i in tasks:
            store.add_task(i)
        expected_task_info = store.make_dict(task1)
        actual_task_info = store.get_task_info(task1.id)
        assert actual_task_info == expected_task_info


class TestFlask:
    def test_basic_connection(self):
        r = requests.get(f"{localhost}/test-connection/?test=basic-connection")
        r.raise_for_status()
        response = r.text
        assert response == "hello world"

    def test_args_dot_get_method(self):
        message = "sample-for-testing"
        r = requests.get(f"{localhost}/get-task/?taskid={message}")
        r.raise_for_status()
        response = r.text
        assert response == "passing connection test"

    def test_flask_instantiating_Store_class(self):
        r = requests.get(f"{localhost}/test-connection/?test=database")
        # r.raise_for_status()
        response = r.text
        assert response == "no errors thrown in Store instantiation"
