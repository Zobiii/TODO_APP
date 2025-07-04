import tkinter as tk
from ui.main_window import ToDoWindow

def main():
    root = tk.Tk()
    app = ToDoWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()