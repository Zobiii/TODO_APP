import tkinter as tk
from tkinter import messagebox
from models.task_manager import TaskManager
from ui.styles import AppStyles

class ToDoWindow:
    def __init__(self, root):
        self.root = root
        self.task_manager = TaskManager()
        self.styles = AppStyles()
        
        self.setup_window()
        self.create_widgets()
        self.refresh_listbox()

    def setup_window(self):
        self.root.title("✓ Meine ToDo-Liste")
        self.root.geometry("700x400")
        self.root.configure(bg=self.styles.bg_color)

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Meine ToDo-Liste",
            font=self.styles.title_font,
            bg=self.styles.bg_color,
            fg=self.styles.text_color,
            pady=15
        )
        title_label.pack()

        input_Frame = tk.Frame(self.root, bg=self.styles.bg_color)
        input_Frame.pack(pady=10, padx=20, fill='x')

        self.task_entry = tk.Entry(
            input_Frame,
            width=30,
            font=self.styles.entry_font,
            relief='flat',
            bd=2,
            highlightthickness=2,
            highlightcolor=self.styles.primary_color
        )
        self.task_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        self.add_button = tk.Button(
            input_Frame,
            text="➕ Hinzufügen",
            command=self.add_task,
            font=self.styles.button_font,
            bg=self.styles.primary_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.add_button.pack(side='right')

        list_frame = tk.Frame(self.root, bg=self.styles.bg_color)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        self.task_listbox = tk.Listbox(
            list_frame,
            font=self.styles.entry_font,
            relief='flat',
            bd=2,
            highlightthickness=1,
            highlightcolor=self.styles.secondary_color,
            selectbackground=self.styles.secondary_color,
            selectforeground='white',
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        button_frame = tk.Frame(self.root, bg=self.styles.bg_color)
        button_frame.pack(pady=10, padx=20, fill='x')

        self.delete_button = tk.Button(
            button_frame, 
            text="🗑️ Löschen", 
            command=self.delete_task,
            font=self.styles.button_font,
            bg=self.styles.danger_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.delete_button.pack(side='left')

        self.clear_button = tk.Button(
            button_frame, 
            text="🧹 Alle löschen", 
            command=self.clear_all_tasks,
            font=self.styles.button_font,
            bg=self.styles.warning_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.clear_button.pack(side='left', padx=(10, 0))

        # Task Counter
        self.counter_label = tk.Label(
            button_frame,
            text="",
            font=("Arial", 9),
            bg=self.styles.bg_color,
            fg=self.styles.text_color
        )
        self.counter_label.pack(side='right')

        self.add_hover_effects()

    def add_hover_effects(self):
        def on_enter(e, button, color):
            button.config(bg=color)
        
        def on_leave(e, button, original_color):
            button.config(bg=original_color)

        # Hover-Effekte für Buttons
        self.add_button.bind("<Enter>", lambda e: on_enter(e, self.add_button, '#45a049'))
        self.add_button.bind("<Leave>", lambda e: on_leave(e, self.add_button, self.styles.primary_color))
        
        self.delete_button.bind("<Enter>", lambda e: on_enter(e, self.delete_button, '#da190b'))
        self.delete_button.bind("<Leave>", lambda e: on_leave(e, self.delete_button, self.styles.danger_color))
        
        self.clear_button.bind("<Enter>", lambda e: on_enter(e, self.clear_button, '#e68900'))
        self.clear_button.bind("<Leave>", lambda e: on_leave(e, self.clear_button, self.styles.warning_color))

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_manager.add_task(task)
            self.task_entry.delete(0, tk.END)
            self.refresh_listbox()
        else:
            messagebox.showwarning("Hinweis", "Bitte eine Aufgabe eingeben!")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_manager.delete_task(selected[0])
            self.refresh_listbox()
        else:
            messagebox.showwarning("Hinweis", "Bitte eine Aufgabe auswählen!")

    def clear_all_tasks(self):
        if self.task_manager.has_tasks():
            result = messagebox.askyesno("Bestätigung", "Alle Aufgaben löschen?")
            if result:
                self.task_manager.clear_all_tasks()
                self.refresh_listbox()

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_tasks()
        for i, task in enumerate(tasks, 1):
            self.task_listbox.insert(tk.END, f"{i}. {task}")
        
        task_count = len(tasks)
        self.counter_label.config(text=f"📊 {task_count} Aufgabe(n)")