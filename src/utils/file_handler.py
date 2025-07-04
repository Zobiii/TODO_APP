import json
import os

class FileHandler:
    def __init__(self, filename="tasks.json"):
        self.files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
        self.filename = os.path.join(self.files_dir, filename)

        os.makedirs(self.files_dir, exist_ok=True)

    def load_tasks(self):
        print(f"[FileHandler] Loading tasks from file {self.filename}")
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                    print("[FileHandler] Tasks loaded successfully.")
                    return tasks
            except (json.JSONDecodeError, IOError):
                print("[FileHandler] Error loading tasks.")
                return []
        print("[FileHandler] No tasks file found.")
        return []

    def save_tasks(self, tasks):
        print(f"[FileHandler] Saving tasks to file: {self.filename}")
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
                print("[FileHandler] Tasks saved successfully.")
        except IOError:
            print("[FileHandler] Error saving tasks.")