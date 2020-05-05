import sqlite3
from pathlib import Path


class Dbconnector:
    def __init__(self, database: Path):
        self.conn = sqlite3.connect(database=database)
        self.cursor = self.conn.cursor()
        self._create_schema()

    def _create_schema(self):
        script = """
                BEGIN TRANSACTION;
                DROP TABLE IF EXISTS tasks;
                CREATE TABLE tasks (
                    taskid TEXT PRIMARY KEY,
                    task TEXT NOT NULL,
                    desc TEXT NOT NULL 
                );
                DROP TABLE IF EXISTS tasklog;
                CREATE TABLE tasklog (
                    taskid TEXT,
                    finished INTEGER, -- 0 = false, 1 = true
                    FOREIGN KEY(taskid) REFERENCES tasks(taskid)
                );
                COMMIT TRANSACTION;
        """
        self.cursor.executescript(script)
