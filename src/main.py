import tkinter as tk
from ui.main_window import ToDoWindow

def main():
    print("[Main] Starting the application...")
    root = tk.Tk()
    print("[Main] Tkinter root window created.")
    app = ToDoWindow(root)
    print("[Main] ToDoWindow initialized.")
    root.mainloop()
    print("[Main] Application main loop terminated.")

if __name__ == "__main__":
    print("[Main] Running main funtion.")
    main()