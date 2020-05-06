from backend.create_database import Dbconnector
from collections import namedtuple
from typing import List

Task = namedtuple("Task", ["id", "short", "desc", "done"], defaults=[0])


class Store:
    def __init__(self):
        self.db: Dbconnector = Dbconnector()
        self.db.load_schema()
        self.conn = self.db.conn
        self.cursor = self.conn.cursor()

    def _commit(self) -> None:
        self.db.commit()

    def _close(self) -> None:
        self.conn.close()

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

    def get_all_tasks(self) -> List[dict]:
        script = """
            SELECT tasks.taskid, short, desc, done
            FROM tasks
            INNER JOIN tasklog ON tasks.taskid = tasklog.taskid;
        """
        raw_data = self.cursor.execute(script).fetchall()
        all_tasks = []
        for i in raw_data:
            all_tasks.append(
                {"taskid": i[0], "short": i[1], "desc": i[2], "done": i[3]}
            )
        return all_tasks


if __name__ == "__main__":
    store = Store()

    # mocked tasks
    task1 = Task(
        "12346781326895423", "pomodoro project", "write a sample coding project",
    )
    task2 = Task("778906475648709", "learn flask", "read all the books on flask")
    task3 = Task(
        "7579021236573678932", "teach python", "teach somebody how to use python"
    )
    tasks = [task1, task2, task3]
    for i in tasks:
        store.add_task(i)
    print("Added sample tasks to database")
