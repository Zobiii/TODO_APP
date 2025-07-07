from utils.database_handler import DatabaseHandler


class TaskManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        raw_tasks = self.db_handler.get_all_tasks()
        return [
            {"id": task[0], "text": task[1], "completed": task[2]} for task in raw_tasks
        ]

    def add_task(self, task, due_date=None):
        print(f"[TaskManager] Adding task: {task}")
        self.db_handler.add_task(task, due_date)
        self.tasks = self._load_tasks()

    def delete_task(self, task_id):
        print(f"[TaskManager] Deleting task at index: {task_id}")
        self.db_handler.delete_task(task_id)
        self.tasks = self._load_tasks()

    def clear_all_tasks(self):
        print("[TaskManager] Clearing all tasks.")
        self.db_handler.clear_all_tasks()
        self.tasks = self._load_tasks()

    def get_tasks(self, sort_by="id ASC"):
        tasks_data = self.db_handler.get_all_tasks(order_by=sort_by)
        tasks = [
            {
                "id": row[0],
                "text": row[1],
                "completed": bool(row[2]),
                "due_date": row[3],
            }
            for row in tasks_data
        ]
        return tasks

    def has_tasks(self):
        task_count = self.db_handler.connection.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()
        return task_count[0] > 0 if task_count else False

    def toggle_task_completion(self, task_id):
        print(f"[TaskManager] Toggling completion for task at index: {task_id}")

        tasks = self.get_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            new_status = not task["completed"]
            self.db_handler.update_task_completion(task_id, new_status)
        self._load_tasks()

    def clear_completed_tasks(self):
        print("[TaskManager] Clearing completed tasks.")
        self.db_handler.clear_completed_tasks()
        self.tasks = self._load_tasks()

    def get_completed_count(self):
        completed_tasks = self.db_handler.connection.execute(
            "SELECT COUNT(*) FROM tasks WHERE completed = ?", (True,)
        ).fetchone()
        return completed_tasks[0] if completed_tasks else 0

    def get_pending_count(self):
        pending_tasks = self.db_handler.connection.execute(
            "SELECT COUNT(*) FROM tasks WHERE completed = ?", (False,)
        ).fetchone()
        return pending_tasks[0] if pending_tasks else 0

    def update_task_text(self, task_id, new_text):
        self.db_handler.update_task_text(new_text, task_id)
        self._load_tasks()

    def get_total_count(self):
        return self.db_handler.get_total_count()
