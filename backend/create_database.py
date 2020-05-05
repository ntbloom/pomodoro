import sqlite3
from pathlib import Path

class Dbconnector:
    def __init__(self, database: Path):
        self.conn = sqlite3.connect(database=database)
        self.cursor = self.conn.cursor()


