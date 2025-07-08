from utils.database_handler import DatabaseHandler
import logging


class TaskManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def add_task(self, task, due_date=None, category="Allgemein", priority=1):
        logging.info(
            f"Adding task '{task}' with due date: {due_date}, category: {category}, priority: {priority}"
        )
        self.db_handler.add_task(task, due_date, category, priority)

    def delete_task(self, task_id):
        logging.info(f"Deleting task with id: {task_id}")
        self.db_handler.delete_task(task_id)

    def clear_all_tasks(self):
        logging.info(f"Deleting all tasks")
        self.db_handler.clear_all_tasks()

    def get_tasks(self, sort_by="id ASC", category_filter=None):
        tasks_data = self.db_handler.get_all_tasks(
            order_by=sort_by, category_filter=category_filter
        )
        tasks = [
            {
                "id": row[0],
                "text": row[1],
                "completed": bool(row[2]),
                "due_date": row[3],
                "category": row[4] if len(row) > 4 else "Allgemein",
                "priority": row[5] if len(row) > 5 else 1,
            }
            for row in tasks_data
        ]
        return tasks

    def has_tasks(self):
        return self.get_total_count() > 0

    def toggle_task_completion(self, task_id):
        logging.info(f"Toggle completion for task with id: {task_id}")

        tasks = self.get_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            new_status = not task["completed"]
            self.db_handler.update_task_completion(task_id, new_status)

    def clear_completed_tasks(self):
        logging.info(f"Deleting all completed tasks")
        self.db_handler.clear_completed_tasks()

    def get_completed_count(self):
        return self.db_handler.get_completed_count()

    def get_pending_count(self):
        return self.db_handler.get_pending_count()

    def update_task_text(self, task_id, new_text):
        logging.info(f"Update task with id '{task_id}' to: '{new_text}'")
        self.db_handler.update_task_text(new_text, task_id)

    def get_total_count(self):
        return self.db_handler.get_total_count()

    def get_categories(self):
        return self.db_handler.get_categories()

    def get_task_by_id(self, task_id):
        """Gibt eine Aufgabe anhand ihrer ID zurück"""
        query = "SELECT * FROM tasks WHERE id = ?"
        result = self.db_handler.execute_query(query, (task_id,))
        if result:
            return result[0]  # Gibt die erste Aufgabe zurück (sollte eindeutig sein)
        return None
