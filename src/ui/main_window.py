from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QListWidget,
    QLineEdit,
    QMessageBox,
    QLabel,
    QScrollBar,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.task_manager import TaskManager
from ui.styles import AppStyles


class ToDoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.styles = AppStyles()

        self.setWindowTitle("ToDo-Liste")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(
            f"background-color: {self.styles.bg_color}; color: {self.styles.text_color};"
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()
        self.refresh_listbox()

    def create_widgets(self):
        # Titel
        title_label = QLabel("Meine ToDo-Liste")
        title_label.setFont(QFont(self.styles.title_font[0], self.styles.title_font[1]))
        title_label.setStyleSheet(f"color: {self.styles.text_color}; padding: 0px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # Eingabefeld und Hinzufügen-Button
        input_frame = QVBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Neue Aufgabe hinzufügen...")
        self.task_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {self.styles.bg_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: {self.styles.text_color};
            }}
        """
        )
        self.task_input.returnPressed.connect(self.add_task)
        input_frame.addWidget(self.task_input)

        self.add_button = QPushButton("➕ Hinzufügen")
        self.add_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.styles.primary_color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """
        )
        self.add_button.clicked.connect(self.add_task)
        input_frame.addWidget(self.add_button)

        self.layout.addLayout(input_frame)

        # Aufgabenliste mit Scrollbar
        list_frame = QVBoxLayout()
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {self.styles.bg_color};
                border: 1px solid {self.styles.secondary_color};
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: {self.styles.text_color};
            }}
            QListWidget::item:selected {{
                background-color: {self.styles.secondary_color};
                color: white;
            }}
        """
        )
        self.task_list.itemDoubleClicked.connect(self.toggle_task_completion)
        list_frame.addWidget(self.task_list)

        self.task_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.task_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.layout.addLayout(list_frame)

        # Buttons für Aktionen
        button_frame = QVBoxLayout()

        first_row = QVBoxLayout()
        self.toggle_button = QPushButton("✅ Erledigt")
        self.toggle_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.styles.success_color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #1e7e34;
            }}
        """
        )
        self.toggle_button.clicked.connect(self.toggle_task_completion)
        first_row.addWidget(self.toggle_button)

        self.delete_button = QPushButton("🗑️ Löschen")
        self.delete_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.styles.danger_color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """
        )
        self.delete_button.clicked.connect(self.delete_task)
        first_row.addWidget(self.delete_button)

        button_frame.addLayout(first_row)

        second_row = QVBoxLayout()
        self.clear_button = QPushButton("🧹 Alle löschen")
        self.clear_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.styles.warning_color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #e68900;
            }}
        """
        )
        self.clear_button.clicked.connect(self.clear_all_tasks)
        second_row.addWidget(self.clear_button)

        self.clear_completed_button = QPushButton("🗂️ Erledigte löschen")
        self.clear_completed_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.styles.info_color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #138496;
            }}
        """
        )
        self.clear_completed_button.clicked.connect(self.clear_completed_tasks)
        second_row.addWidget(self.clear_completed_button)

        self.counter_label = QLabel("")
        self.counter_label.setStyleSheet(
            f"color: {self.styles.text_color}; font-size: 12px;"
        )
        second_row.addWidget(self.counter_label)

        button_frame.addLayout(second_row)
        self.layout.addLayout(button_frame)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            print(f"[MainWindow] Adding task: {task}")
            self.task_manager.add_task(task)
            self.task_input.clear()
            self.refresh_listbox()
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe eingeben!")

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                index = self.task_list.row(item)
                print(f"[MainWindow] Deleting task at index: {index}")
                self.task_manager.delete_task(index)
            self.refresh_listbox()
        else:
            QMessageBox.showwarning("Hinweis", "Bitte eine Aufgabe auswählen!")

    def clear_all_tasks(self):
        print("[MainWindow] Clearing all tasks.")
        if self.task_manager.has_tasks():
            result = QMessageBox.question(
                self,
                "Bestätigung",
                "Alle Aufgaben löschen?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if result == QMessageBox.StandardButton.Yes:
                self.task_manager.clear_all_tasks()
                self.refresh_listbox()

    def refresh_listbox(self):
        print("[MainWindow] Refreshing task list.")
        self.task_list.clear()
        tasks = self.task_manager.get_tasks()  # Ensure this returns a valid list

        if not isinstance(tasks, list):
            print("[Error] get_tasks() did not return a list.")
            tasks = []  # Fallback to an empty list

        for i, task in enumerate(tasks, 1):
            display_text = (
                f"✅ {task['text']}" if task["completed"] else f"⏳ {task['text']}"
            )
            self.task_list.addItem(display_text)

        total_count = len(tasks)
        completed_count = self.task_manager.get_completed_count()
        pending_count = self.task_manager.get_pending_count()

        counter_text = f"📊 Gesamt: {total_count} | ✅ Erledigt: {completed_count} | ⏳ Offen: {pending_count}"
        self.counter_label.setText(counter_text)

    def toggle_task_completion(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                print("[MainWindow] Toggling task completion.")
                self.task_manager.toggle_task_completion(self.task_list.row(item))
            self.refresh_listbox()
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")

    def toggle_task_completion(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                index = self.task_list.row(item)
                print("[MainWindow] Toggling task completion.")
                self.task_manager.toggle_task_completion(index)
            self.refresh_listbox()
        else:
            QMessageBox.showwarning("Hinweis", "Bitte eine Aufgabe auswählen!")

    def clear_completed_tasks(self):
        print("[MainWindow] Clearing completed tasks.")
        completed_count = self.task_manager.get_completed_count()
        if completed_count > 0:
            result = QMessageBox.question(
                self,
                "Bestätigung",
                f"{completed_count} erledigte Aufgaben löschen?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if result == QMessageBox.StandardButton.Yes:
                self.task_manager.clear_completed_tasks()
                self.refresh_listbox()
        else:
            QMessageBox.information(
                self, "Info", "Keine erledigten Aufgaben vorhanden!"
            )
