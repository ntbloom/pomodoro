from create_database import Dbconnector
from collections import namedtuple
from typing import List, Set
from pathlib import Path
import json

Task = namedtuple("Task", ["id", "short", "desc", "done"], defaults=[0])


class Store:
    def __init__(self, database: Path):
        self.db: Dbconnector = Dbconnector(database)
        self.conn = self.db.conn
        self.cursor = self.conn.cursor()

    def _commit(self) -> None:
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def add_task(self, task: Task) -> None:
        """adds task to database"""
        tasks_script = """
                 INSERT INTO tasks VALUES (?,?,?);
         """
        self.cursor.execute(tasks_script, (task.id, task.short, task.desc))

        tasklog_script = """
                INSERT INTO tasklog (taskid, done) 
                    VALUES (?, ?);
        """
        self.cursor.execute(tasklog_script, (task.id, task.done))
        self._commit()

    def mark_task_as_finished(self, taskid: str) -> None:
        """marks a task as finished"""
        self.cursor.execute(
            """
                UPDATE tasklog
                    SET done = 1
                    WHERE taskid = ?;
        """,
            [taskid],
        )
        self._commit()

    @staticmethod
    def make_dict(task: Task) -> dict:
        """restructures a namedtuple as a dictionary"""
        new_dict = {
            "id": task.id,
            "short": task.short,
            "desc": task.desc,
            "done": task.done,
        }
        return new_dict

    @staticmethod
    def _parse_raw_query_results(results: List[tuple]) -> dict:
        """helper method for turning raw query results into structured dict"""
        ordered_results = {
            "id": results[0],
            "short": results[1],
            "desc": results[2],
            "done": results[3],
        }
        return ordered_results

    @staticmethod
    def create_task_from_json(data: json) -> Task:
        """converts raw json into a Task object"""
        data_as_dict = {} 
        if type(data) is dict:
            data_as_dict = data
        else:
            data_as_dict = json.loads(data)
        id = data_as_dict["id"]
        short = data_as_dict["short"]
        desc = data_as_dict["desc"]
        done = data_as_dict["done"]
        return Task(id, short, desc, done)

    def get_all_tasks(self) -> List[dict]:
        script = """
                SELECT tasks.taskid, short, desc, done
                FROM tasks
                INNER JOIN tasklog ON tasks.taskid = tasklog.taskid;
        """
        raw_data = self.cursor.execute(script).fetchall()
        all_tasks = []
        for i in raw_data:
            all_tasks.append(self._parse_raw_query_results(i))
        return all_tasks

    def get_all_taskids(self) -> Set:
        """returns a set of all taskids"""
        script = """
                SELECT taskid
                FROM tasks;
        """
        taskids = set()
        raw_data = self.cursor.execute(script).fetchall()
        for entry in raw_data:
            taskids.add(entry[0])

        return taskids

    def get_task_info(self, taskid: str) -> dict:
        """returns relevant info about a task from its taskid"""
        script = """
                SELECT tasks.taskid, short, desc, done
                FROM tasks
                INNER JOIN tasklog ON tasks.taskid = tasklog.taskid
                WHERE tasks.taskid = ?;
        """
        raw_info = self.cursor.execute(script, (taskid,)).fetchall()[0]
        return self._parse_raw_query_results(raw_info)
