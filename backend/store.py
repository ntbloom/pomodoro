from backend.create_database import Dbconnector
from pathlib import Path
from collections import namedtuple

Task = namedtuple("Task", ["id", "short", "long"])


class Store:
    def __init__(self):
        self.db = Dbconnector()
        self.db.load_schema()
        self.conn = self.db.conn
        self.cursor = self.conn.cursor()

    def _commit(self):
        self.db.commit()

    def add_task(self, task: Task):
        """adds task to database"""
        a = task.id
        b = task.short
        c = task.long
        tasks_script = """
                 INSERT INTO tasks VALUES (?,?,?);
         """
        self.cursor.execute(tasks_script, task)

        tasklog_script = """
                INSERT INTO tasklog (taskid, finished) 
                    VALUES (?, 0);
        """
        self.cursor.execute(tasklog_script, (task.id,))
        self._commit()
