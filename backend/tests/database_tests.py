import pytest
from pathlib import Path
from backend.create_database import Dbconnector

DATABASE = Path("../pomodoro.db")


class TestDatabaseFunctionality:
    def test_connection(self):
        d = Dbconnector(DATABASE)
        result = d.cursor.execute("""SELECT 1+1;""").fetchone()[0]
        assert result == 2
