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
        self.root.geometry("800x600")
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

        self.task_listbox.bind('<Double-1>', lambda e: self.toggle_task_completion())

        button_frame = tk.Frame(self.root, bg=self.styles.bg_color)
        button_frame.pack(pady=10, padx=20, fill='x')

        first_row = tk.Frame(button_frame, bg=self.styles.bg_color)
        first_row.pack(fill='x', pady=(0, 5))

        self.toggle_button = tk.Button(
            first_row,
            text="✅ Erledigt",
            command=self.toggle_task_completion,
            font=self.styles.button_font,
            bg=self.styles.success_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.toggle_button.pack(side='left')

        self.delete_button = tk.Button(
            first_row, 
            text="🗑️ Löschen", 
            command=self.delete_task,
            font=self.styles.button_font,
            bg=self.styles.danger_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.delete_button.pack(side='left', padx=(10, 0))

        second_row = tk.Frame(button_frame, bg=self.styles.bg_color)
        second_row.pack(fill='x')

        self.clear_button = tk.Button(
            second_row, 
            text="🧹 Alle löschen", 
            command=self.clear_all_tasks,
            font=self.styles.button_font,
            bg=self.styles.warning_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.clear_button.pack(side='left')

        self.clear_completed_button = tk.Button(
            second_row,
            text="🗂️ Erledigte löschen",
            command=self.clear_completed_tasks,
            font=self.styles.button_font,
            bg=self.styles.info_color,
            fg='white',
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        self.clear_completed_button.pack(side='left', padx=(10, 0))

        # Task Counter
        self.counter_label = tk.Label(
            second_row,
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

        buttons = [
            (self.add_button, '#45a049', self.styles.primary_color),
            (self.toggle_button, '#28a745', self.styles.success_color),  
            (self.delete_button, '#da190b', self.styles.danger_color),
            (self.clear_button, '#e68900', self.styles.warning_color),
            (self.clear_completed_button, '#138496', self.styles.info_color)  
        ]

        for button, hover_color, original_color in buttons:
            button.bind("<Enter>", lambda e, b=button, hc=hover_color: on_enter(e, b, hc))
            button.bind("<Leave>", lambda e, b=button, oc=original_color: on_leave(e, b, oc))

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
            if task["completed"]:
                display_text = f"✅ {i}. {task['text']}"
                self.task_listbox.insert(tk.END, display_text)
                self.task_listbox.itemconfig(i-1, {'fg': self.styles.completed_color})
            else:
                display_text = f"⏳ {i}. {task['text']}"
                self.task_listbox.insert(tk.END, display_text)
        total_count = len(tasks)
        completed_count = self.task_manager.get_completed_count()
        pending_count =  self.task_manager.get_pending_count()

        counter_text = f"📊 Gesamt: {total_count} | ✅ Erledigt: {completed_count} | ⏳ Offen: {pending_count}"
        self.counter_label.config(text=counter_text)

    def toggle_task_completion(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_manager.toggle_task_completion(selected[0])
            self.refresh_listbox()
        else:
            messagebox.showwarning("Hinweis", "Bitte eine Aufgabe auswählen!")
    
    def clear_completed_tasks(self):
        completed_count = self.task_manager.get_completed_count()
        if completed_count > 0:
            result = messagebox.askyesno("Bestätigung", f"{completed_count} erledigte Aufgaben löschen?")
            if result:
                self.task_manager.clear_completed_tasks()
                self.refresh_listbox()
        else:
            messagebox.showinfo("Info", "Keine erledigten Aufgaben vorhanden!")