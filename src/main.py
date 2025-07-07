from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import ToDoWindow
import os


def main():
    print("[Main] Starting the application...")
    app = QApplication([])

    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "../assets/notepad_icon.png")
    app.setWindowIcon(QIcon(icon_path))

    window = ToDoWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    print("[Main] Running main funtion.")
    main()
