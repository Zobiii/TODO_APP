from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import ToDoWindow
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("todo_app.log"), logging.StreamHandler()],
)


def main():
    app = QApplication([])
    logging.info(f"Starting the application.")

    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "../assets/notepad_icon.png")
    app.setWindowIcon(QIcon(icon_path))

    window = ToDoWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    logging.info(f"Running main function")
    main()
