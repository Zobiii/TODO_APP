from utils.file_handler import FileHandler

class TaskManager:
    def __init__(self):
        self.file_handler = FileHandler()
        raw_tasks = self.file_handler.load_tasks()
        self.tasks = self._convert_old_tasks(raw_tasks)

    def add_task(self, task):
        print(f"[TaskManager] Adding task: {task}")
        task_obj = {
            "text": task,
            "completed": False
        }

        self.tasks.append(task_obj)
        self.file_handler.save_tasks(self.tasks)

    def delete_task(self, index):
        print(f"[TaskManager] Deleting task at index: {index}")
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.file_handler.save_tasks(self.tasks)

    def clear_all_tasks(self):
        print("[TaskManager] Clearing all tasks.")
        self.tasks.clear()
        self.file_handler.save_tasks(self.tasks)

    def get_tasks(self):
        return self.tasks

    def has_tasks(self):
        return len(self.tasks) > 0
    
    def toggle_task_completion(self, index):
        print(f"[TaskManager] Toggling completion for task at index: {index}")
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.file_handler.save_tasks(self.tasks)

    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.file_handler.save_tasks(self.tasks)

    def get_completed_count(self):
        return sum(1 for task in self.tasks if task["completed"])
    
    def get_pending_count(self):
        return sum(1 for task in self.tasks if not task["completed"])
    
    def _convert_old_tasks(self, tasks):
        """Konvertiert alte String-Tasks zu neuen Task-Objekten"""
        converted_tasks = []
        for task in tasks:
            if isinstance(task, str):
                # Alte String-Tasks zu Objekten konvertieren
                converted_tasks.append({
                    "text": task,
                    "completed": False
                })
            elif isinstance(task, dict):
                # Neue Task-Objekte bleiben unverändert
                converted_tasks.append(task)
        return converted_tasks