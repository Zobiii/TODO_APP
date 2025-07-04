from utils.file_handler import FileHandler

class TaskManager:
    def __init__(self):
        self.file_handler = FileHandler()
        self.tasks = self.file_handler.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.file_handler.save_tasks(self.tasks)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.file_handler.save_tasks(self.tasks)

    def clear_all_tasks(self):
        self.tasks.clear()
        self.file_handler.save_tasks(self.tasks)

    def get_tasks(self):
        return self.tasks

    def has_tasks(self):
        return len(self.tasks) > 0