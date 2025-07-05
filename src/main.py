from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import ToDoWindow

def main():
    print("[Main] Starting the application...")
    app = QApplication([])
    app.setWindowIcon(QIcon("c:/Users/lechn/Desktop/todo_app/assets/notepad_icon.png"))
    window = ToDoWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    print("[Main] Running main funtion.")
    main()