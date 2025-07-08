import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
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
        self._initialize_managers()
        self._setup_constants()
        self._setup_window()
        self._setup_ui()
        self._initialize_data()

    # ===== INITIALIZATION METHODS =====
    def _initialize_managers(self):
        """Initialisiert Task Manager und Styles"""
        self.task_manager = TaskManager()
        self.styles = AppStyles()

    def _setup_constants(self):
        """Definiert Konstanten für Sortierung und Prioritäten"""
        self.sort_options = {
            "Sortieren nach: Datum": "due_date ASC, id ASC",
            "Sortieren nach: Alphabet": "text ASC",
            "Sortieren nach: Status": "completed DESC, id ASC",
            "Sortieren nach: Priorität": "priority DESC, id ASC",
        }
        self.priority_options = {"🔴 Hoch": 3, "🟡 Mittel": 2, "🟢 Niedrig": 1}

    def _setup_window(self):
        """Konfiguriert das Hauptfenster"""
        self.setWindowTitle("ToDo-Liste")
        self.setGeometry(100, 100, 800, 900)
        self.setStyleSheet(
            f"background-color: {self.styles.bg_color}; color: {self.styles.text_color};"
        )

    def _setup_ui(self):
        """Erstellt die gesamte Benutzeroberfläche"""
        self.create_menu_bar()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.create_widgets()
        self.status_bar = self.statusBar()

    def _initialize_data(self):
        """Lädt initiale Daten"""
        self.refresh_listbox()
        self._update_category_filter()

    # ===== UI CREATION METHODS =====
    def create_widgets(self):
        """Erstellt alle UI-Widgets"""
        self._create_title()
        self._create_input_section()
        self._create_filter_section()
        self._create_task_list()
        self._create_action_buttons()

    def _create_title(self):
        """Erstellt den Titel"""
        title_label = QLabel("Meine ToDo-Liste")
        title_label.setFont(QFont(self.styles.title_font[0], self.styles.title_font[1]))
        title_label.setStyleSheet(f"color: {self.styles.text_color}; padding: 0px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

    def _create_input_section(self):
        """Erstellt den Eingabebereich für neue Aufgaben"""
        input_frame = QVBoxLayout()

        # Task Input
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Neue Aufgabe hinzufügen...")
        self.task_input.setStyleSheet(self._get_line_edit_stylesheet())
        self.task_input.returnPressed.connect(self.add_task)
        input_frame.addWidget(self.task_input)

        # Category and Priority
        input_frame.addLayout(self._create_category_priority_inputs())

        # Date and Add Button
        input_frame.addLayout(self._create_date_section())

        self.layout.addLayout(input_frame)

    def _create_category_priority_inputs(self):
        """Erstellt Kategorie- und Prioritätseingaben"""
        category_priority_frame = QHBoxLayout()

        # Category
        cat_label = QLabel("🏷️ Kategorie:")
        cat_label.setStyleSheet(f"color: {self.styles.text_color}; font-size: 14px;")
        category_priority_frame.addWidget(cat_label)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(
            ["Allgemein", "Arbeit", "Privat", "Einkaufen", "Sport", "Familie"]
        )
        self.category_input.setStyleSheet(self._get_combo_box_stylesheet())
        category_priority_frame.addWidget(self.category_input)

        # Priority
        prio_label = QLabel("⚡ Priorität:")
        prio_label.setStyleSheet(f"color: {self.styles.text_color}; font-size: 14px;")
        category_priority_frame.addWidget(prio_label)

        self.priority_input = QComboBox()
        self.priority_input.addItems(self.priority_options.keys())
        self.priority_input.setCurrentIndex(1)  # Standard: Mittel
        self.priority_input.setStyleSheet(self._get_combo_box_stylesheet())
        category_priority_frame.addWidget(self.priority_input)

        return category_priority_frame

    def _create_date_section(self):
        """Erstellt Datum- und Hinzufügen-Button"""
        date_button_frame = QVBoxLayout()

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setStyleSheet(self._get_date_edit_stylesheet())
        date_button_frame.addWidget(self.due_date_input)

        self.add_button = QPushButton("➕ Hinzufügen")
        self.add_button.setStyleSheet(self._get_primary_button_stylesheet())
        self.add_button.clicked.connect(self.add_task)
        date_button_frame.addWidget(self.add_button)

        return date_button_frame

    def _create_filter_section(self):
        """Erstellt Filter- und Sortierbereich"""
        # Category Filter
        filter_frame = QVBoxLayout()
        filter_label = QLabel("🏷️ Kategorie filtern:")
        filter_label.setStyleSheet(
            f"color: {self.styles.text_color}; font-size: 14px; font-weight: bold;"
        )
        filter_frame.addWidget(filter_label)

        self.category_filter = QComboBox()
        self.category_filter.setStyleSheet(self._get_filter_combo_stylesheet())
        self.category_filter.currentIndexChanged.connect(self.refresh_listbox)
        filter_frame.addWidget(self.category_filter)
        self.layout.addLayout(filter_frame)

        # Sort Options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(self.sort_options.keys())
        self.sort_combo.setStyleSheet(self._get_filter_combo_stylesheet())
        self.sort_combo.currentIndexChanged.connect(self.refresh_listbox)
        self.layout.addWidget(self.sort_combo)

    def _create_task_list(self):
        """Erstellt die Aufgabenliste"""
        list_frame = QVBoxLayout()
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(self._get_list_widget_stylesheet())
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_context_menu)

        self.task_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.task_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        list_frame.addWidget(self.task_list)
        self.layout.addLayout(list_frame)

    def _create_action_buttons(self):
        """Erstellt die Action-Buttons"""
        button_frame = QVBoxLayout()

        self.clear_button = QPushButton("🧹 Alle löschen")
        self.clear_button.setStyleSheet(self._get_warning_button_stylesheet())
        self.clear_button.clicked.connect(self.clear_all_tasks)
        button_frame.addWidget(self.clear_button)

        self.clear_completed_button = QPushButton("🗂️ Erledigte löschen")
        self.clear_completed_button.setStyleSheet(self._get_info_button_stylesheet())
        self.clear_completed_button.clicked.connect(self.clear_completed_tasks)
        button_frame.addWidget(self.clear_completed_button)

        self.counter_label = QLabel("")
        self.counter_label.setStyleSheet(
            f"color: {self.styles.text_color}; font-size: 12px;"
        )
        button_frame.addWidget(self.counter_label)

        self.layout.addLayout(button_frame)

    # ===== STYLESHEET METHODS =====
    def _get_menu_bar_stylesheet(self):
        """Stylesheet für die Menüleiste"""
        return f"""
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

    def _get_line_edit_stylesheet(self):
        """Stylesheet für Eingabefelder"""
        return f"""
            QLineEdit {{
                background-color: {self.styles.bg_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: {self.styles.text_color};
            }}
        """

    def _get_combo_box_stylesheet(self):
        """Stylesheet für ComboBoxen"""
        return f"""
            QComboBox {{
                background-color: {self.styles.bg_color};
                border: 2px solid {self.styles.primary_color};
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: {self.styles.text_color};
                min-width: 120px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.styles.bg_color};
                color: {self.styles.text_color};
                border: 1px solid {self.styles.secondary_color};
            }}
        """

    def _get_filter_combo_stylesheet(self):
        """Stylesheet für Filter-ComboBoxen"""
        return f"""
            QComboBox {{
                background-color: {self.styles.bg_color};
                border: 1px solid {self.styles.secondary_color};
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: {self.styles.text_color};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.styles.bg_color};
                color: {self.styles.text_color};
                border: 1px solid {self.styles.secondary_color};
            }}
        """

    def _get_date_edit_stylesheet(self):
        """Stylesheet für Datum-Eingabe"""
        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        icon_path = os.path.join(project_root, "icons", "calendar.svg").replace(
            "\\", "/"
        )

        return f"""
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
                background-color: transparent;
                padding-bottom: 10px;
                padding-top: 20px;
                padding-left: 5px;
            }}
            QCalendarWidget QAbstractItemView:item:selected {{
                color: {self.styles.warning_color};
            }}
        """

    def _get_primary_button_stylesheet(self):
        """Stylesheet für primäre Buttons"""
        return f"""
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

    def _get_warning_button_stylesheet(self):
        """Stylesheet für Warning-Buttons"""
        return f"""
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

    def _get_info_button_stylesheet(self):
        """Stylesheet für Info-Buttons"""
        return f"""
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

    def _get_list_widget_stylesheet(self):
        """Stylesheet für die Aufgabenliste"""
        return f"""
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

    def _get_context_menu_stylesheet(self):
        """Stylesheet für Kontextmenü"""
        return f"""
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
                border: 1px solid {self.styles.text_color};
            }}
            QMenu::item:selected {{
                background-color: {self.styles.secondary_color};
                color: white;
                border: 1px solid {self.styles.text_color};
            }}
            QMenu::separator {{
                height: 2px;
                background: {self.styles.text_color};
                margin: 4px 4px;
            }}
        """

    def _switch_theme_stylesheet(self):
        return f"background-color: {self.styles.bg_color}; color: {self.styles.text_color};"

    # ===== EVENT HANDLER METHODS =====

    def show_context_menu(self, position):
        """Zeigt das Kontextmenü für Aufgaben"""
        item = self.task_list.itemAt(position)
        if not item:
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        all_tasks = self.task_manager.get_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)
        if not current_task:
            return

        context_menu = QMenu(self)
        context_menu.setStyleSheet(self._get_context_menu_stylesheet())

        # Actions erstellen
        if not current_task["completed"]:
            toggle_action = QAction("✅ Als erledigt markieren", self)
        else:
            toggle_action = QAction("↩️ Auf 'offen' setzen", self)

        toggle_action.triggered.connect(lambda: self.toggle_task_completion(item))
        context_menu.addAction(toggle_action)

        edit_action = QAction("✏️ Bearbeiten", self)
        edit_action.triggered.connect(lambda: self.edit_task(item))
        context_menu.addAction(edit_action)

        context_menu.addSeparator()

        delete_action = QAction("🗑️ Löschen", self)
        delete_action.triggered.connect(lambda: self.delete_task(item))
        context_menu.addAction(delete_action)

        context_menu.exec(self.task_list.mapToGlobal(position))

    def create_menu_bar(self):
        """Erstellt die Menüleiste mit Backup-Optionen"""
        menubar = self.menuBar()
        menubar.setStyleSheet(self._get_menu_bar_stylesheet())

        backup_menu = menubar.addMenu("Backup")

        create_backup_action = QAction("📂 Backup erstellen", self)
        create_backup_action.triggered.connect(self.create_backup)
        backup_menu.addAction(create_backup_action)

        restore_backup_action = QAction("🔄 Backup wiederherstellen", self)
        restore_backup_action.triggered.connect(self.restore_backup)
        backup_menu.addAction(restore_backup_action)

        theme_menu = menubar.addMenu("Themes")

        dark_theme_action = QAction("🌙 Dunkles Theme", self)
        dark_theme_action.triggered.connect(lambda: self.switch_theme("dark"))
        theme_menu.addAction(dark_theme_action)

        # Helles Theme
        light_theme_action = QAction("☀️ Helles Theme", self)
        light_theme_action.triggered.connect(lambda: self.switch_theme("light"))
        theme_menu.addAction(light_theme_action)

    # ===== TASK MANAGEMENT METHODS =====

    def add_task(self):
        """Fügt eine neue Aufgabe hinzu"""
        task = self.task_input.text().strip()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.currentText() or "Allgemein"
        priority = self.priority_options[self.priority_input.currentText()]

        if task:
            self.task_manager.add_task(task, due_date, category, priority)
            all_tasks = self.task_manager.get_tasks(sort_by="id DESC")

            if all_tasks:
                new_task = all_tasks[0]
                self.add_task_to_ui(new_task)

            self._reset_input_fields()
            self.status_bar.showMessage("✅ Aufgabe hinzugefügt", 5000)
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe eingeben!")

    def delete_task(self, item=None):
        """Löscht eine Aufgabe"""
        if not item:
            item = self.task_list.currentItem()

        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.task_manager.delete_task(task_id)

            self.remove_task_from_ui(task_id)

            self.status_bar.showMessage("🗑️ Aufgabe gelöscht", 5000)
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")

    def toggle_task_completion(self, item=None):
        """Ändert den Erledigungsstatus einer Aufgabe"""
        if not item:
            item = self.task_list.currentItem()

        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.task_manager.toggle_task_completion(task_id)
            self.refresh_listbox()
        else:
            QMessageBox.warning(self, "Hinweis", "Bitte eine Aufgabe auswählen!")

    def edit_task(self, item):
        """Bearbeitet eine Aufgabe"""
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
                updated_task = self.task_manager.get_task_by_id(task_id)
                self._update_task_in_ui(task_id, updated_task)

    def clear_all_tasks(self):
        """Löscht alle Aufgaben"""
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
                self.update_category_filter()

    def clear_completed_tasks(self):
        """Löscht alle erledigten Aufgaben - OPTIMIERT"""
        completed_count = self.task_manager.get_completed_count()
        if completed_count > 0:
            result = QMessageBox.question(
                self,
                "Bestätigung",
                f"{completed_count} erledigte Aufgaben löschen?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if result == QMessageBox.StandardButton.Yes:
                # Aus der Datenbank löschen
                self.task_manager.clear_completed_tasks()

                # Nur erledigte Aufgaben aus der UI entfernen
                self.clear_completed_tasks_from_ui()
        else:
            QMessageBox.information(
                self, "Info", "Keine erledigten Aufgaben vorhanden!"
            )

    def switch_theme(self, theme_name):
        if self.styles.switch_theme(theme_name):
            self.setStyleSheet(self._switch_theme_stylesheet())
            self._refresh_all_styles()
            theme_display = "🌙 Dunkles" if theme_name == "dark" else "☀️ Helles"
            self.status_bar.showMessage(f"{theme_display} Theme aktiviert", 3000)

    # ===== BACKUP METHODS =====

    def create_backup(self):
        """Erstellt ein Backup der Datenbank"""
        backup_path, _ = QFileDialog.getSaveFileName(
            self, "Backup erstellen", "todo", "Datenbank (*.db)"
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
        """Stellt ein Backup der Datenbank wieder her"""
        backup_path, _ = QFileDialog.getOpenFileName(
            self, "Backup wiederherstellen", "", "Datenbank (*.db)"
        )
        if backup_path:
            success = self.task_manager.db_handler.restore_database(backup_path)
            if success:
                self.refresh_listbox()
                self.update_category_filter()
                self.status_bar.showMessage(
                    "✅ Backup erfolgreich wiederhergestellt", 5000
                )
            else:
                QMessageBox.critical(
                    self, "Fehler", "Backup konnte nicht wiederhergestellt werden."
                )

    # ===== DATA UPDATE METHODS =====

    def refresh_listbox(self):
        """Aktualisiert die Aufgabenliste basierend auf Sortierung und Filterung"""
        current_sort_text = self.sort_combo.currentText()
        sort_by_clause = self.sort_options.get(current_sort_text, "id ASC")

        category_filter = self.category_filter.currentText()
        if category_filter == "Alle":
            category_filter = None

        self.task_list.clear()
        tasks = self.task_manager.get_tasks(
            sort_by=sort_by_clause, category_filter=category_filter
        )

        if not isinstance(tasks, list):
            tasks = []

        today = QDate.currentDate()
        for task in tasks:
            display_text = self._format_task_display(task)
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, task["id"])
            self.task_list.addItem(item)

            # Farben für überfällige Aufgaben
            self._apply_task_colors(item, task, today)

        self._update_counter()

    def _format_task_display(self, task):
        """Formatiert die Anzeige einer Aufgabe"""
        due_date_str = task.get("due_date")
        category = task.get("category", "Allgemein")
        priority = task.get("priority", 1)

        priority_icon = "🔴" if priority == 3 else "🟡" if priority == 2 else "🟢"
        status_icon = "✅" if task["completed"] else "⏳"

        display_text = f"{status_icon} {priority_icon} [{category}] {task['text']}"

        if due_date_str:
            display_text += f"  (Fällig: {due_date_str})"

        return display_text

    def _apply_task_colors(self, item, task, today):
        """Wendet Farben basierend auf Fälligkeitsdatum an"""
        due_date_str = task.get("due_date")
        if due_date_str and not task["completed"]:
            due_date = QDate.fromString(due_date_str, "yyyy-MM-dd")
            if due_date.isValid():
                if due_date < today:
                    item.setForeground(QColor(self.styles.danger_color))
                elif due_date == today:
                    item.setForeground(QColor(self.styles.warning_color))

    def _update_counter(self):
        """Aktualisiert die Aufgaben-Statistiken"""
        total_count = self.task_manager.get_total_count()
        completed_count = self.task_manager.get_completed_count()
        pending_count = self.task_manager.get_pending_count()

        counter_text = f"📊 Gesamt: {total_count} | ✅ Erledigt: {completed_count} | ⏳ Offen: {pending_count}"
        self.counter_label.setText(counter_text)

    def _update_category_filter(self):
        """Aktualisiert die Kategorie-Filter ComboBox"""
        current_selection = self.category_filter.currentText()
        self.category_filter.clear()

        try:
            categories = ["Alle"] + self.task_manager.get_categories()
            self.category_filter.addItems(categories)

            index = self.category_filter.findText(current_selection)
            if index >= 0:
                self.category_filter.setCurrentIndex(index)
        except Exception:
            self.category_filter.addItems(["Alle", "Allgemein"])

    def _refresh_all_styles(self):
        """Aktualisiert alle Styles nach Theme-Wechsel"""
        # Menüleiste aktualisieren
        self.menuBar().setStyleSheet(self._get_menu_bar_stylesheet())

        # Eingabefeld aktualisieren
        if hasattr(self, "task_input"):
            self.task_input.setStyleSheet(self._get_line_edit_stylesheet())

        # ComboBoxen aktualisieren
        if hasattr(self, "category_input"):
            self.category_input.setStyleSheet(self._get_combo_box_stylesheet())
        if hasattr(self, "priority_input"):
            self.priority_input.setStyleSheet(self._get_combo_box_stylesheet())
        if hasattr(self, "category_filter"):
            self.category_filter.setStyleSheet(self._get_filter_combo_stylesheet())
        if hasattr(self, "sort_combo"):
            self.sort_combo.setStyleSheet(self._get_filter_combo_stylesheet())

        # Datum-Eingabe aktualisieren
        if hasattr(self, "due_date_input"):
            self.due_date_input.setStyleSheet(self._get_date_edit_stylesheet())

        # Buttons aktualisieren
        if hasattr(self, "add_button"):
            self.add_button.setStyleSheet(self._get_primary_button_stylesheet())
        if hasattr(self, "clear_button"):
            self.clear_button.setStyleSheet(self._get_warning_button_stylesheet())
        if hasattr(self, "clear_completed_button"):
            self.clear_completed_button.setStyleSheet(
                self._get_info_button_stylesheet()
            )

        # Liste aktualisieren
        if hasattr(self, "task_list"):
            self.task_list.setStyleSheet(self._get_list_widget_stylesheet())

        # Labels aktualisieren
        for child in self.findChildren(QLabel):
            if "color:" in child.styleSheet():
                current_style = child.styleSheet()
                # Ersetze alte Textfarbe mit neuer
                new_style = current_style.replace(
                    "color: #ecf0f1", f"color: {self.styles.text_color}"
                ).replace("color: #2c3e50", f"color: {self.styles.text_color}")
                child.setStyleSheet(new_style)

        # Aufgabenliste neu laden um Farben zu aktualisieren
        self.refresh_listbox()

    def _reset_input_fields(self):
        """Setzt die Eingabefelder zurück"""
        self.task_input.clear()
        self.category_input.setCurrentText("Allgemein")
        self.priority_input.setCurrentIndex(1)

    # ===== EFFICIENT UI UPDATE METHODS =====

    def add_task_to_ui(self, task_data):
        display_text = self._format_task_display(task_data)
        item = QListWidgetItem(display_text)
        item.setData(Qt.ItemDataRole.UserRole, task_data["id"])

        today = QDate.currentDate()
        self._apply_task_colors(item, task_data, today)

        self.task_list.addItem(item)

        self._update_counter()

    def remove_task_from_ui(self, task_id):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                self.task_list.takeItem(i)
                self._update_counter()
                break

    def _update_task_in_ui(self, task_id, updated_task_data):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                display_text = self._format_task_display(updated_task_data)
                item.setText(display_text)

                # Farben neu anwenden
                today = QDate.currentDate()
                self._apply_task_colors(item, updated_task_data, today)

                self._update_counter()
                break

    def clear_completed_tasks_from_ui(self):
        """Entfernt nur die erledigten Aufgaben aus der UI"""
        items_to_remove = []

        # Sammle Items, die entfernt werden sollen
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item:
                task_id = item.data(Qt.ItemDataRole.UserRole)
                task_data = self.task_manager.get_task_by_id(task_id)
                if task_data and task_data.get("completed", False):
                    items_to_remove.append(i)

        # Entferne Items (rückwärts, um Indizes nicht zu verschieben)
        for i in reversed(items_to_remove):
            self.task_list.takeItem(i)

        self._update_counter()
