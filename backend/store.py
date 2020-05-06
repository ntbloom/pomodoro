from backend.create_database import Dbconnector
from pathlib import Path
from collections import namedtuple

Task = namedtuple("Task", ["id", "short", "desc", "done"], defaults=[0])


class Store:
    def __init__(self):
        self.db: Dbconnector = Dbconnector()
        self.db.load_schema()
        self.conn = self.db.conn
        self.cursor = self.conn.cursor()

    def _commit(self) -> None:
        self.db.commit()

    def add_task(self, task: Task) -> None:
        """adds task to database"""
        a = task.id
        b = task.short
        c = task.desc
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

    def finish_task(self, taskid: str) -> None:
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
