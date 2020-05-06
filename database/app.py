from database.store.store import Store, Task
from flask import Flask, request, jsonify
from pathlib import Path

DATABASE = Path("./tests/test_database.db")
app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "hello world"


@app.route("/get-task/", methods=["GET"])
def get_task():
    """simple getter method using REST"""
    taskid = request.args.get("taskid")
    print(f"taskid={taskid}")
    if taskid == "sample-for-testing":
        return "passing connection test"
    return "write the rest of this method"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
