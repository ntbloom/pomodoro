from datastore.store import Store, Task
from flask import Flask, request, Request, Response, jsonify
from flask_cors import CORS, cross_origin
import json
from pathlib import Path
import os

filepath = Path("./test_database.db")
DATABASE = os.path.abspath(filepath)
print(f"DATABASE={DATABASE}")

app = Flask(__name__)
CORS(app)


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
    task = store.get_task_info(taskid)
    store.close()
    return jsonify(task)


@app.route("/add-task/", methods=["POST", "GET"])
@cross_origin()
def add_task() -> Response:
    print(f"\n\n{request.headers}\n\n{request.is_json}")
    payload = request.get_json()
    print(f"\n\nPAYLOAD={payload}\n\n")
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
    response = {"tasks": all_tasks}
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
