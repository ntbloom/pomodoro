import sqlite3


class Dbconnector:
    def __init__(self):
        self.conn = sqlite3.connect(database="./pomorodo.db")
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
                    done INTEGER, -- 0 = false, 1 = true
                    FOREIGN KEY(taskid) REFERENCES tasks(taskid)
                );
                COMMIT TRANSACTION;
        """
        self.cursor.executescript(script)

    def commit(self) -> None:
        """commits transactions"""
        self.conn.commit()
