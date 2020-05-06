import sqlite3

DATABASE = "./database.db"


class Dbconnector:
    def __init__(self):
        self.conn = sqlite3.connect(database=DATABASE)
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
