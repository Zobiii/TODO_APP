import sqlite3
import os


class DatabaseHandler:
    def __init__(self, db_name="todo.db"):
        doc_path = os.path.join(os.path.expanduser("~"), "Documents")
        app_folder_path = os.path.join(doc_path, "Todo_App")
        os.makedirs(app_folder_path, exist_ok=True)
        self.db_path = os.path.join(app_folder_path, db_name)
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    completed BOOLEAN NOT NULL
                )
            """
            )

    def add_task(self, text):
        with self.connection:
            self.connection.execute(
                "INSERT INTO tasks (text, completed) VALUES (?, ?)", (text, False)
            )

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task_completion(self, task_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id)
            )

    def get_all_tasks(self):
        with self.connection:
            return self.connection.execute(
                "SELECT id, text, completed FROM tasks"
            ).fetchall()

    def clear_all_tasks(self):
        with self.connection:
            self.connection.execute("DELETE FROM tasks")

    def clear_completed_tasks(self):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE completed = ?", (True,))
