from database.store.store import Store, Task
from flask import Flask, request, jsonify
from pathlib import Path
import os

filepath = Path("./tests/test_database.db")
DATABASE = os.path.abspath(filepath)
print(f"DATABASE={DATABASE}")
app = Flask(__name__)


@app.route("/test-connection/", methods=["GET"])
def hello() -> str:
    test = request.args.get("test")
    if test == "basic-connection":
        return "hello world"
    if test == "database":
        return "connected to database"
    return ""


@app.route("/get-task/", methods=["GET"])
def get_task():
    """simple getter method using REST"""
    taskid = request.args.get("taskid")
    if taskid == "sample-for-testing":
        return "passing connection test"
    return "write the rest of this method"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
