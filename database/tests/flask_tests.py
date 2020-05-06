"""
-setup for general test-driven development. incremental tests assure code has 100% coverage.
-for production systems database would be production server like Postgresql, etc. with mockups for test environments
-in this case we just re-use the "production" sqlite file

to run test suite, run `python -m pytest *.py` in a terminal
"""


from datastore.create_database import Dbconnector
from datastore.store import Task, Store
import pytest
import requests
from pathlib import Path
import os
import json

filename = Path("./test_database.db")
DATABASE = os.path.abspath(filename)
DB = Dbconnector(DATABASE)
localhost = "http://127.0.0.1:5000"

# mocked tasks -- in production would use either greater qty of tasks or use property-based testing
task1 = Task("12346781326895423", "pomodoro project", "write a sample coding project",)
task2 = Task("778906475648709", "learn flask", "read all the books on flask")
task3 = Task("7579021236573678932", "teach python", "teach somebody how to use python")


class TestFlask:
    @pytest.fixture(scope="function", autouse=True)
    def make_clean_database_each_time(self):
        DB.load_schema()
        yield

    def test_basic_connection(self):
        r = requests.get(f"{localhost}/test-connection/?test=basic-connection")
        r.raise_for_status()
        response = r.text
        assert response == "hello world"

    def test_flask_instantiating_Store_class(self):
        r = requests.get(f"{localhost}/test-connection/?test=database")
        r.raise_for_status()
        response = r.text
        assert response == "no errors thrown in Store instantiation"

    def test_flask_database_connection(self):
        r = requests.get(f"{localhost}/test-connection/?test=two-plus-two")
        r.raise_for_status()
        response = r.text
        assert response == "4"

    def test_basic_task_id_requests(self):
        message = "sample-for-testing"
        r = requests.get(f"{localhost}/get-task/?taskid={message}")
        r.raise_for_status()
        response = r.text
        assert response == "passing connection test"

    def test_get_task_from_taskid(self):
        store = Store(DATABASE)
        task = task1
        store.add_task(task)
        r = requests.get(f"{localhost}/get-task/?taskid={task.id}")
        r.raise_for_status()
        actual_response = json.loads(r.text)
        expected_response = Store.make_dict(task)
        assert actual_response == expected_response

    def test_taskid_not_found(self):
        store = Store(DATABASE)
        bad_id = "this-id-doesnt-exist"
        r = requests.get(f"{localhost}/get-task/?taskid={bad_id}")
        assert r.status_code == 404

    def test_add_task(self):
        store = Store(DATABASE)
        payload = json.dumps(Store.make_dict(task1))
        post = requests.post(f"{localhost}/add-task/", json=(payload))
        post.raise_for_status()
        r = requests.get(f"{localhost}/get-task/?taskid={task1.id}")
        actual_response = json.loads(r.text)
        expected_response = Store.make_dict(task1)
        assert actual_response == expected_response

    def test_flask_marks_task_as_finished(self):
        store = Store(DATABASE)
        task = task1
        store.add_task(task)
        assert task.done == 0, f"task {task.id} is already finished"
        post = requests.post(f"{localhost}/finish-task/?taskid={task.id}")
        post.raise_for_status()
        r = requests.get(f"{localhost}/get-task/?taskid={task.id}")
        done = json.loads(r.text)["done"]
        assert done == 1

    def test_flask_gets_all_tasks(self):
        store = Store(DATABASE)
        test_tasks = [task1, task2, task3]
        for i in test_tasks:
            store.add_task(i)
        task_dict_list = [Store.make_dict(i) for i in test_tasks]
        expected = {"tasks": task_dict_list}
        r = requests.get(f"{localhost}/get-all-tasks")
        r.raise_for_status()
        actual = json.loads(r.text)
        assert actual == expected
