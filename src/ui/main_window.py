import os
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
    QInputDialog,
    QComboBox,
    QDateEdit,
    QListWidgetItem,
    QMenu,
    QFileDialog,
)
from PyQt6.QtGui import QFont, QColor, QAction
from PyQt6.QtCore import Qt, QDate
from models.task_manager import TaskManager
from ui.styles import AppStyles


class ToDoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.styles = AppStyles()
        self.sort_options = {
            "Sortieren nach: Datum": "due_date ASC, id ASC",
            "Sortieren nach: Alphabet": "text ASC",
            "Sortieren nach: Status": "completed DESC, id ASC",
        }

        self.setWindowTitle("ToDo-Liste")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(
            f"background-color: {self.styles.bg_color}; color: {self.styles.text_color};"
        )

        self.create_menu_bar()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()
        self.refresh_listbox()
        self.status_bar = self.statusBar()

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

        date_button_frame = QVBoxLayout()

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())

        # Erstelle einen robusten, absoluten Pfad zum Icon
        script_dir = os.path.dirname(__file__)  # Pfad zum ui-Ordner
        project_root = os.path.abspath(
            os.path.join(script_dir, "..", "..")
        )  # Gehe zwei Ebenen hoch zum Projekt-Root
        icon_path = os.path.join(project_root, "icons", "calendar.svg").replace(
            "\\", "/"
        )

        self.due_date_input.setStyleSheet(
            f"""
            QDateEdit {{
                background-color: {self.styles.bg_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: {self.styles.text_color};
            }}  
            QDateEdit::drop-down {{
                border-left: 1px solid gray;
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 36px; 
            }}
            QDateEdit::drop-down:hover {{
                background-color: {self.styles.primary_color};
                border-top-right-radius: 2px;
                border-bottom-right-radius: 2px;
            }}
            QDateEdit::down-arrow {{
                image: url({icon_path});
                width: 20px;
                height: 20px;
            }}
            QCalendarWidget QWidget {{
                background-color: {self.styles.bg_color};
                color: {self.styles.text_color};
            }}
            QCalendarWidget QToolButton {{
                color: {self.styles.text_color};
                background-color: transparent;
                border: 2px solid {self.styles.primary_color};
                border-radius: 16px;
                margin: 7px;
                padding: 5px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {self.styles.secondary_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 16px;
            }}
            QCalendarWidget QToolButton::menu-indicator {{
                image: none;
            }}
            QCalendarWidget QMenu {{
                background-color: {self.styles.bg_color}; 
                color: {self.styles.text_color}; 
                border: 2px solid {self.styles.primary_color}; 
                border-radius: 5px; 
            }}
            QCalendarWidget QMenu::item {{
                padding: 5px 10px; 
                background-color: transparent; 
                color: {self.styles.text_color}; 
                border-bottom: 1px solid {self.styles.primary_color};
            }}  
            QCalendarWidget QAbstractItemView {{
                background-color: transparent;
                color: {self.styles.text_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 16px;
                gridline-color: transparent;
                padding-bottom: 0px;
                
            }}

            QCalendarWidget QAbstractItemView:item {{
                background-color:  transparent;
                padding-bottom: 10px;
                padding-top: 20px;
                padding-left: 5px;
            }}
            QCalendarWidget QAbstractItemView:item:selected {{
                color: {self.styles.warning_color};
            }}
            """
        )

        date_button_frame.addWidget(self.due_date_input)

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

        input_frame.addLayout(date_button_frame)

        self.layout.addLayout(input_frame)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(self.sort_options.keys())
        self.sort_combo.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {self.styles.bg_color};
                border: 1px solid {self.styles.secondary_color};
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """
        )
        self.sort_combo.currentIndexChanged.connect(self.refresh_listbox)
        self.layout.addWidget(self.sort_combo)

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
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_context_menu)
        list_frame.addWidget(self.task_list)

        self.task_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.task_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.layout.addLayout(list_frame)

        # Buttons für Aktionen
        button_frame = QVBoxLayout()
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

    def show_context_menu(self, position):
        item = self.task_list.itemAt(position)
        if not item:
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        all_tasks = self.task_manager.get_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)
        if not current_task:
            return

        context_menu = QMenu(self)
        context_menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {self.styles.bg_color};
                border: 2px solid {self.styles.text_color};
                border-radius: 5px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 4px;
                margin: 2px;
                color: black;
                border: 1px solid {self.styles.text_color}; /* Rahmen für jeden Button */
            }}
            QMenu::item:selected {{
                background-color: {self.styles.secondary_color};
                color: white;
                border: 1px solid {self.styles.text_color}; /* Rahmenfarbe bei Hover anpassen */
            }}
            QMenu::separator {{
                height: 2px;
                background: {self.styles.text_color};
                margin: 4px 4px;
            }}
            """
        )

        # Aktion: Erledigen / Rückgängig
        if not current_task["completed"]:
            toggle_action = QAction("✅ Als erledigt markieren", self)
        else:
            toggle_action = QAction("↩️ Auf 'offen' setzen", self)

        toggle_action.triggered.connect(lambda: self.toggle_task_completion(item))
        context_menu.addAction(toggle_action)

        # Aktion: Bearbeiten
        edit_action = QAction("✏️ Bearbeiten", self)
        edit_action.triggered.connect(lambda: self.edit_task(item))
        context_menu.addAction(edit_action)

        context_menu.addSeparator()

        # Aktion: Löschen
        delete_action = QAction("🗑️ Löschen", self)
        delete_action.triggered.connect(lambda: self.delete_task(item))
        context_menu.addAction(delete_action)

        context_menu.exec(self.task_list.mapToGlobal(position))

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(
            f"""
            QMenuBar {{
                background-color: {self.styles.bg_color};
                color: {self.styles.text_color};
                border-bottom: 1px solid {self.styles.secondary_color};
                padding: 4px;
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.styles.secondary_color};
            }}
            QMenu {{
                background-color: {self.styles.bg_color};
                color: {self.styles.text_color};
                border: 1px solid {self.styles.secondary_color};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 4px;
                margin: 2px;
            }}
            QMenu::item:selected {{
                background-color: {self.styles.secondary_color};
            }}
        """
        )

        backup_menu = menubar.addMenu("Backup")
        create_backup_action = QAction("📂 Backup erstellen", self)
        create_backup_action.triggered.connect(self.create_backup)
        backup_menu.addAction(create_backup_action)

        restore_backup_action = QAction("🔄 Backup wiederherstellen", self)
        restore_backup_action.triggered.connect(self.restore_backup)
        backup_menu.addAction(restore_backup_action)

    def add_task(self):
        task = self.task_input.text().strip()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")

        if task:
            self.task_manager.add_task(task, due_date)
            self.task_input.clear()
            self.status_bar.showMessage("✅ Aufgabe hinzugefügt", 5000)
            self.refresh_listbox()
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe eingeben!")

    def delete_task(self, item=None):
        if not item:
            item = self.task_list.currentItem()

        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.task_manager.delete_task(task_id)
            self.refresh_listbox()
            self.status_bar.showMessage("🗑️ Aufgabe gelöscht", 5000)
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")

    def clear_all_tasks(self):
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
        """Aktualisiert die Aufgabenliste basierend auf der aktuellen Sortierung."""

        current_sort_text = self.sort_combo.currentText()
        sort_by_clause = self.sort_options.get(current_sort_text, "id ASC")

        self.task_list.clear()
        tasks = self.task_manager.get_tasks(sort_by=sort_by_clause)

        if not isinstance(tasks, list):
            tasks = []

        today = QDate.currentDate()
        for task in tasks:
            due_date_str = task.get("due_date")
            display_text = (
                f"✅ {task['text']}" if task["completed"] else f"⏳ {task['text']}"
            )

            if due_date_str:
                display_text += f"  (Fällig: {due_date_str})"

            item = QListWidgetItem(display_text)
            # Speichere die eindeutige Task-ID im Item
            item.setData(Qt.ItemDataRole.UserRole, task["id"])
            self.task_list.addItem(item)

            if due_date_str and not task["completed"]:
                due_date = QDate.fromString(due_date_str, "yyyy-MM-dd")
                if due_date.isValid():
                    if due_date < today:
                        item.setForeground(QColor(self.styles.danger_color))
                    elif due_date == today:
                        item.setForeground(QColor(self.styles.warning_color))

        # Redundanten Codeblock entfernen
        total_count = self.task_manager.get_total_count()
        completed_count = self.task_manager.get_completed_count()
        pending_count = self.task_manager.get_pending_count()

        counter_text = f"📊 Gesamt: {total_count} | ✅ Erledigt: {completed_count} | ⏳ Offen: {pending_count}"
        self.counter_label.setText(counter_text)

    def toggle_task_completion(self, item=None):
        if not item:
            item = self.task_list.currentItem()

        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.task_manager.toggle_task_completion(task_id)
            self.refresh_listbox()
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")

    def clear_completed_tasks(self):
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

    def edit_task(self, item):
        if not item:
            item = self.task_list.currentItem()

        if not item:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        all_tasks = self.task_manager.get_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)

        if current_task:
            current_text = current_task["text"]
            new_text, ok = QInputDialog.getText(
                self, "Aufgabe bearbeiten", "Neuer Text:", text=current_text
            )

            if ok and new_text.strip():
                self.task_manager.update_task_text(task_id, new_text.strip())
                self.refresh_listbox()

    def create_backup(self):
        backup_path, _ = QFileDialog.getSaveFileName(
            self, "Backup erstellen", "todo_app", "Datenbank (*.db)"
        )
        if backup_path:
            success = self.task_manager.db_handler.backup_db(backup_path)
            if success:
                self.status_bar.showMessage("✅ Backup erfolgreich erstellt", 5000)
            else:
                QMessageBox.critical(
                    self, "Fehler", "Backup konnte nicht erstellt werden."
                )

    def restore_backup(self):
        backup_path, _ = QFileDialog.getOpenFileName(
            self, "Backup wiederherstellen", "", "Datenbank (*.db)"
        )
        if backup_path:
            success = self.task_manager.db_handler.restore_database(backup_path)
            if success:
                self.refresh_listbox()
                self.status_bar.showMessage(
                    "✅ Backup erfolgreich wiederhergestellt", 5000
                )
            else:
                QMessageBox.critical(
                    self, "Fehler", "Backup konnte nicht wiederhergestellt werden."
                )
