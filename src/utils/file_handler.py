import json
import os

class FileHandler:
    def __init__(self):
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        self.app_folder = os.path.join(documents_folder, "ToDo_App")  # Unterordner "ToDo_App"
        self.filename = os.path.join(self.app_folder, "tasks.json")  # Pfad zur tasks.json

        # Überprüfen, ob der Ordner existiert, ansonsten erstellen
        if not os.path.exists(self.app_folder):
            print(f"[FileHandler] Creating folder: {self.app_folder}")
            os.makedirs(self.app_folder)

    def load_tasks(self):
        print(f"[FileHandler] Loading tasks from file: {self.filename}")
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