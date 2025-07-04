import json
import os

class FileHandler:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self, tasks):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
        except IOError:
            print("Fehler beim Speichern der Aufgabe")