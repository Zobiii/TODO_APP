import json
import os

class FileHandler:
    def __init__(self, filename="tasks.json"):
        self.files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
        self.filename = os.path.join(self.files_dir, filename)

        os.makedirs(self.files_dir, exist_ok=True)

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_tasks(self, tasks):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
        except IOError:
            print("Fehler beim Speichern der Aufgaben")