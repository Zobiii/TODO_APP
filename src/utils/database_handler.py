import sqlite3
import os
import shutil
import logging


class DatabaseHandler:
    def __init__(self, db_name="todo.db"):
        doc_path = os.path.join(os.path.expanduser("~"), "Documents")
        app_folder_path = os.path.join(doc_path, "Todo_App")
        os.makedirs(app_folder_path, exist_ok=True)
        self.db_path = os.path.join(app_folder_path, db_name)
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()
        self._add_due_date_column_if_not_exists()

    def backup_db(self, backup_path):
        try:
            shutil.copy(self.db_path, backup_path)
            logging.info(f"Backup erfolgreich erstellt: {backup_path}")
            return True
        except Exception as e:
            logging.info(f"Fehler bei der Backuperstellung {e}")
            return False

    def restore_database(self, backup_path):
        try:
            shutil.copy(backup_path, self.db_path)
            logging.info(f"Backup erfolgreich wiederhergestellt: {backup_path}")
            return True
        except Exception as e:
            logging.info(f"Fehler bei der Wiederherstellung des Backups: {e}")
            return False

    def _create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    completed BOOLEAN NOT NULL,
                    due_date TEXT
                )
            """
            )

    def add_task(self, text, due_date=None):
        with self.connection:
            self.connection.execute(
                "INSERT INTO tasks (text, completed, due_date) VALUES (?, ?, ?)",
                (text, False, due_date),
            )

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task_completion(self, task_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id)
            )

    def get_all_tasks(self, order_by="id ASC"):
        """
        Get all tasks, sorted by a specific column.
        :param order_by: SQL ORDER BY clause (e.g., 'text ASC', 'completed DESC').
        """
        with self.connection:
            query = (
                f"SELECT id, text, completed, due_date FROM tasks ORDER BY {order_by}"
            )
            return self.connection.execute(query).fetchall()

    def clear_all_tasks(self):
        with self.connection:
            self.connection.execute("DELETE FROM tasks")

    def clear_completed_tasks(self):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE completed = ?", (True,))

    def update_task_text(self, new_text, task_id):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks SET text = ? WHERE id = ?", (new_text, task_id)
            )

    def get_total_count(self):
        """Gibt die Gesamtzahl der Aufgaben zurück."""
        with self.connection:
            # fetchone()[0] gibt den ersten Wert der ersten Zeile zurück
            return self.connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    def _add_due_date_column_if_not_exists(self):
        """Prüft, ob die 'due_date' Spalte existiert und fügt sie bei Bedarf hinzu."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA table_info(tasks)")
            columns = [info[1] for info in cursor.fetchall()]
            if "due_date" not in columns:
                print("Spalte 'due_date' nicht gefunden. Füge sie hinzu...")
                cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
                self.connection.commit()
                print("Spalte 'due_date' zur Datenbank hinzugefügt.")

    def get_pending_count(self):
        with self.connection:
            return self.connection.execute(
                "SELECT COUNT(*) FROM tasks WHERE completed = ?", (False,)
            ).fetchone()[0]

    def get_completed_count(self):
        with self.connection:
            return self.connection.execute(
                "SELECT COUNT(*) FROM tasks WHERE completed = ?", (True,)
            ).fetchone()[0]
