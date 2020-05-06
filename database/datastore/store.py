from create_database import Dbconnector
from collections import namedtuple
from typing import List
from pathlib import Path

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
            "taskid": task.id,
            "short": task.short,
            "desc": task.desc,
            "done": task.done,
        }
        return new_dict

    @staticmethod
    def _parse_raw_query_results(results: List[tuple]) -> dict:
        """helper method for turning raw query results into structured dict"""
        ordered_results = {
            "taskid": results[0],
            "short": results[1],
            "desc": results[2],
            "done": results[3],
        }
        return ordered_results

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
