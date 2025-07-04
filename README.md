# 📝 ToDoApp – A Simple Desktop Task Manager

**ToDoApp** is a minimal yet powerful desktop application for managing your daily tasks. Built with Python and Tkinter, it provides a clean, responsive interface and a modular codebase to keep your task management intuitive and fast.

---

## 🚀 Features

- ✅ Add and manage tasks with one click or press `Enter`
- 📋 Tasks are shown in a scrollable list with clear status indicators
- 🔄 Automatically saves your tasks locally (JSON file)
- 💡 Visual feedback for completed vs. pending tasks
- 🧩 Modular code structure (UI, models, file utilities)
- 🎨 Customizable styling via a central `styles.py` file

---

## 🖥️ User Interface

The UI is designed with simplicity in mind:

- A header with the app title
- An entry field to type new tasks
- A button to add them
- A listbox showing tasks with icons for **pending** and **done**
- A task summary counter at the bottom

---

## 📁 Project Structure
src/
├── main.py # Entry point for the app
├── files/
│ └── tasks.json # Local task storage (auto-created)
├── models/
│ └── task_manager.py # Core logic for task handling
├── ui/
│ ├── main_window.py # Main application window and event handling
│ └── styles.py # Color and font definitions
└── utils/
  └── file_handler.py # Reads and writes tasks to disk


---

## 🛠️ Requirements

- **Python 3.8+**
- No external packages required – uses built-in modules only

---

## ▶️ How to Run

1. Clone or download this repository
2. Open a terminal in the root directory
3. Run the app:

```bash
python src/main.py
Your task file tasks.json will be created automatically after the first task is added.

💾 Data Format
Tasks are saved in the following structure:

json
Kopieren
Bearbeiten
[
  {
    "text": "Buy groceries",
    "completed": false
  },
  {
    "text": "Finish homework",
    "completed": true
  }
]
Old string-only tasks (e.g. "Buy milk") are automatically converted when loaded.

💡 Planned Features (optional)
Edit existing tasks

Task deadlines and reminders

Theme switcher (light/dark)

Export/import task lists

📄 License
This project is open source. Feel free to use, modify, and share it.

👨‍💻 Author
Made with ❤️ by [Your Name Here] – feel free to improve it!
