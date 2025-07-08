from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import ToDoWindow
import os
import logging
from utils.paths import resource_path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("todo_app.log"), logging.StreamHandler()],
)


def main():
    app = QApplication([])
    logging.info(f"Starting the application")

    icon_path = resource_path("notepad_icon.ico")

    if not os.path.exists(icon_path):
        logging.warning(f"Icon file not found at: {icon_path}")
    else:
        app.setWindowIcon(QIcon(icon_path))

    window = ToDoWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    logging.info(f"Running main function")
    main()
