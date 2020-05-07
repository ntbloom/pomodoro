from store import Store, Task

if __name__=="__main__":
    store = Store("../test_database.db")
    task1 = Task("12346781326895423", "pomodoro project", "write a sample coding project",0)
    task2 = Task("778906475648709", "learn flask", "read all the books on flask",1)
    task3 = Task("7579021236573678932", "teach python", "teach somebody how to use python",0)
    store.db.load_schema()
    store.add_task(task1)
    store.add_task(task2)
    store.add_task(task3)
    store.close()

