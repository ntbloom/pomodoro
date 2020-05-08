import sqlite3
from pathlib import Path


class Dbconnector:
    def __init__(self, database: Path):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def load_schema(self) -> None:
        """creates the tables from the schema"""
        script = """
                BEGIN TRANSACTION;
                DROP TABLE IF EXISTS tasks;
                CREATE TABLE tasks (
                    taskid TEXT PRIMARY KEY,
                    short TEXT NOT NULL,
                    desc TEXT NOT NULL 
                );
                DROP TABLE IF EXISTS tasklog;
                CREATE TABLE tasklog (
                    taskid TEXT,
                    done INTEGER, -- 0 and 1 for false and true
                    FOREIGN KEY(taskid) REFERENCES tasks(taskid)
                );
                COMMIT TRANSACTION;
        """
        self.cursor.executescript(script)
        self.commit()

    def commit(self) -> None:
        """commits transactions"""
        self.conn.commit()

    def close(self) -> None:
        """closes connection to sqlite file"""
        self.conn.close()


if __name__ == "__main__":
    d = Dbconnector("./database.db")
    d.load_schema()
