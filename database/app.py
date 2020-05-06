from datastore.store import Store, Task
from flask import Flask, request, Request, Response
import json
from pathlib import Path
import os

filepath = Path("./test_database.db")
DATABASE = os.path.abspath(filepath)
print(f"DATABASE={DATABASE}")
app = Flask(__name__)


@app.route("/test-connection/", methods=["GET"])
def hello() -> str:
    test = request.args.get("test")
    if test == "basic-connection":
        return "hello world"
    if test == "database":
        store = Store(DATABASE)
        return "no errors thrown in Store instantiation"
    if test == "two-plus-two":
        store = Store(DATABASE)
        four = store.cursor.execute("""SELECT 2+2;""").fetchone()[0]
        return str(four)
    return ""


@app.route("/get-task/", methods=["GET"])
def get_task() -> json:
    """simple getter method using REST"""
    store = Store(DATABASE)
    all_tasks = store.get_all_taskids()
    taskid = request.args.get("taskid")
    if taskid == "sample-for-testing":
        return "passing connection test"
    if taskid not in all_tasks:
        return Response(status=404)
    task = json.dumps(store.get_task_info(taskid))
    store.close()
    return task


@app.route("/add-task/", methods=["POST"])
def add_task() -> Response:
    payload = request.get_json()
    store = Store(DATABASE)
    task = store.create_task_from_json(payload)
    store.add_task(task)
    try:
        assert task.id in store.get_all_taskids()
        return Response(status=200)
    except AssertionError:
        return Response(status=500)
    finally:
        store.close()


@app.route("/finish-task/", methods=["POST"])
def finish_task() -> Response:
    taskid = request.args.get("taskid")
    store = Store(DATABASE)
    store.mark_task_as_finished(taskid)
    try:
        assert store.get_task_info(taskid)["done"] == 1
        return Response(status=200)
    except AssertionError:
        return Response(status=500)
    finally:
        store.close()


@app.route("/get-all-tasks", methods=["GET"])
def get_all_tasks() -> json:
    store = Store(DATABASE)
    all_tasks = store.get_all_tasks()
    response = json.dumps({"tasks": all_tasks})
    print(f"response={response}")
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
