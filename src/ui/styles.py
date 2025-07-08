import json
import os
import logging


class AppStyles:
    def __init__(self, theme="dark"):
        self.current_theme = theme
        self.themes = {
            "dark": {
                "bg_color": "#2c3e50",
                "text_color": "#ecf0f1",
                "primary_color": "#3498db",
                "secondary_color": "#34495e",
                "success_color": "#27ae60",
                "danger_color": "#e74c3c",
                "warning_color": "#f39c12",
                "info_color": "#17a2b8",
                "title_font": ("Arial", 24, "bold"),
                "content_font": ("Arial", 12),
            },
            "light": {
                "bg_color": "#ffffff",
                "text_color": "#2c3e50",
                "primary_color": "#007bff",
                "secondary_color": "#6c757d",
                "success_color": "#28a745",
                "danger_color": "#dc3545",
                "warning_color": "#ffc107",
                "info_color": "#17a2b8",
                "title_font": ("Arial", 24, "bold"),
                "content_font": ("Arial", 12),
            },
        }

        self._apply_theme()
        self._load_user_theme()

    def _apply_theme(self):
        theme_data = self.themes[self.current_theme]
        for key, value in theme_data.items():
            setattr(self, key, value)

    def switch_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self._apply_theme()
            self._save_user_theme()
            return True
        return False

    def get_available_themes(self):
        return list(self.themes.keys())

    def _get_config_path(self):
        doc_path = os.path.join(os.path.expanduser("~"), "Documents")
        app_folder_path = os.path.join(doc_path, "Todo_App")
        os.makedirs(app_folder_path, exist_ok=True)
        logging.info(f"Config Datei in '{app_folder_path}' erstellt/gefunden")
        return os.path.join(app_folder_path, "config.json")

    def _save_user_theme(self):
        try:
            config_path = self._get_config_path()
            config = {"theme": self.current_theme}
            with open(config_path, "w") as f:
                json.dump(config, f)
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Theme-Einstellung: {e}")

    def _load_user_theme(self):
        try:
            config_path = self._get_config_path()
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                    saved_theme = config.get("theme", "dark")
                    if saved_theme in self.themes:
                        self.current_theme = saved_theme
                        self._apply_theme()
        except Exception as e:
            logging.error(f"Fehler beim Laden der Theme-Einstellung: {e}")
