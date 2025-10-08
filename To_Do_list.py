# Import the necessary tkinter library for creating the GUI
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
import datetime

# --- Core Application Class ---

class TodoApp:
    def __init__(self, root):
        """
        Initializes the To-Do List application GUI.
        """
        self.root = root
        self.root.title("✓ Modern To-Do List")
        self.root.geometry("600x550")
        self.root.config(bg="#2c3e50")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Task counter
        self.task_count = 0
        self.completed_count = 0
        
        # Theme management
        self.is_dark_theme = True
        self.themes = {
            'dark': {
                'bg': '#2c3e50',
                'frame_bg': '#34495e',
                'tasks_bg': '#1a252f',
                'entry_bg': '#34495e',
                'entry_fg': '#ecf0f1',
                'listbox_bg': '#34495e',
                'listbox_fg': '#ecf0f1',
                'text_fg': '#ecf0f1',
                'secondary_fg': '#bdc3c7',
                'completed_bg': '#566573',
                'completed_fg': '#85929e'
            },
            'light': {
                'bg': '#ecf0f1',
                'frame_bg': '#ffffff',
                'tasks_bg': '#f8f9fa',
                'entry_bg': '#ffffff',
                'entry_fg': '#2c3e50',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#2c3e50',
                'text_fg': '#2c3e50',
                'secondary_fg': '#7f8c8d',
                'completed_bg': '#d5dbdb',
                'completed_fg': '#7f8c8d'
            }
        }

        # Define fonts
        self.title_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.main_font = tkfont.Font(family="Arial", size=11)
        self.entry_font = tkfont.Font(family="Arial", size=12)
        self.button_font = tkfont.Font(family="Arial", size=10, weight="bold")
        
        # --- Create header ---
        self.create_header()
        
        # --- Create theme toggle ---
        self.create_theme_toggle()
        
        # --- Create and place the main frames ---
        self.frame_input = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.frame_input.pack(pady=15, padx=20, fill=tk.X)

        self.frame_tasks = tk.Frame(self.root, relief=tk.SUNKEN, bd=2)
        self.frame_tasks.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(pady=15)

        # --- Widgets for the input frame ---
        self.input_container = tk.Frame(self.frame_input)
        self.input_container.pack(pady=10, padx=10, fill=tk.X)
        
        self.entry_task = tk.Entry(
            self.input_container, 
            font=self.entry_font, 
            bd=0, 
            relief=tk.FLAT,
            insertbackground="#3498db"
        )
        self.entry_task.pack(side=tk.LEFT, ipady=8, padx=(0, 10), fill=tk.X, expand=True)
        self.entry_task.bind('<Return>', lambda e: self.add_task())
        self.entry_task.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry_task.bind('<FocusOut>', self.on_entry_focus_out)

        self.button_add_task = tk.Button(
            self.input_container,
            text="➕ Add Task",
            command=self.add_task,
            font=self.button_font,
            bg="#27ae60", 
            fg="white", 
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.button_add_task.pack(side=tk.RIGHT)
        self.bind_hover_effects(self.button_add_task, "#27ae60", "#2ecc71")

        # --- Widgets for the tasks frame ---
        self.tasks_container = tk.Frame(self.frame_tasks)
        self.tasks_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.listbox_tasks = tk.Listbox(
            self.tasks_container,
            font=self.main_font,
            bd=0,
            relief=tk.FLAT,
            selectbackground="#3498db",
            selectforeground="white",
            activestyle="none",
            highlightthickness=0
        )
        self.listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_tasks.bind('<Double-Button-1>', lambda e: self.mark_completed())

        self.scrollbar_tasks = tk.Scrollbar(self.tasks_container)
        self.scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_tasks.config(yscrollcommand=self.scrollbar_tasks.set)
        self.scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # --- Widgets for the button frame ---
        self.button_container = tk.Frame(self.frame_buttons)
        self.button_container.pack()
        
        self.button_mark_completed = tk.Button(
            self.button_container,
            text="✓ Complete",
            command=self.mark_completed,
            font=self.button_font,
            bg="#3498db", 
            fg="white", 
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.button_mark_completed.pack(side=tk.LEFT, padx=10)
        self.bind_hover_effects(self.button_mark_completed, "#3498db", "#5dade2")

        self.button_delete_task = tk.Button(
            self.button_container,
            text="🗑️ Delete",
            command=self.delete_task,
            font=self.button_font,
            bg="#e74c3c", 
            fg="white", 
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.button_delete_task.pack(side=tk.LEFT, padx=10)
        self.bind_hover_effects(self.button_delete_task, "#e74c3c", "#ec7063")
        
        self.button_clear_completed = tk.Button(
            self.button_container,
            text="🧹 Clear Completed",
            command=self.clear_completed,
            font=self.button_font,
            bg="#f39c12", 
            fg="white", 
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.button_clear_completed.pack(side=tk.LEFT, padx=10)
        self.bind_hover_effects(self.button_clear_completed, "#f39c12", "#f7dc6f")
        
        # Apply initial theme
        self.apply_theme()

    def create_header(self):
        """Creates a beautiful header with title and task counter"""
        self.header_frame = tk.Frame(self.root, height=80)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        self.header_frame.pack_propagate(False)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="📋 My Tasks",
            font=self.title_font
        )
        self.title_label.pack(pady=10)
        
        self.stats_label = tk.Label(
            self.header_frame,
            text="Total: 0 | Completed: 0",
            font=self.main_font
        )
        self.stats_label.pack()
    
    def create_theme_toggle(self):
        """Creates theme toggle button"""
        theme_frame = tk.Frame(self.root)
        theme_frame.pack(pady=5)
        
        self.theme_button = tk.Button(
            theme_frame,
            text="☀️ Light Mode",
            command=self.toggle_theme,
            font=self.button_font,
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.theme_button.pack()
        self.bind_hover_effects(self.theme_button, "#95a5a6", "#b2bec3")
    
    def bind_hover_effects(self, button, normal_color, hover_color):
        """Adds hover effects to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def toggle_theme(self):
        """Toggles between dark and light themes"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
    
    def apply_theme(self):
        """Applies the current theme to all widgets"""
        theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
        
        # Update root and frames
        self.root.config(bg=theme['bg'])
        self.header_frame.config(bg=theme['bg'])
        self.frame_input.config(bg=theme['frame_bg'])
        self.frame_tasks.config(bg=theme['tasks_bg'])
        self.frame_buttons.config(bg=theme['bg'])
        self.input_container.config(bg=theme['frame_bg'])
        self.tasks_container.config(bg=theme['tasks_bg'])
        self.button_container.config(bg=theme['bg'])
        
        # Update labels
        self.title_label.config(bg=theme['bg'], fg=theme['text_fg'])
        self.stats_label.config(bg=theme['bg'], fg=theme['secondary_fg'])
        
        # Update entry
        self.entry_task.config(bg=theme['entry_bg'], fg=theme['entry_fg'])
        
        # Update listbox
        self.listbox_tasks.config(bg=theme['listbox_bg'], fg=theme['listbox_fg'])
        
        # Update scrollbar
        self.scrollbar_tasks.config(bg=theme['secondary_fg'], troughcolor=theme['tasks_bg'])
        
        # Update theme button
        if self.is_dark_theme:
            self.theme_button.config(text="☀️ Light Mode")
        else:
            self.theme_button.config(text="🌙 Dark Mode")
        
        # Update completed tasks colors
        for i in range(self.listbox_tasks.size()):
            current_bg = self.listbox_tasks.itemcget(i, 'bg')
            if current_bg in ['#d5dbdb', '#566573']:  # Previously completed
                self.listbox_tasks.itemconfig(i, {
                    'bg': theme['completed_bg'],
                    'fg': theme['completed_fg']
                })
            else:
                self.listbox_tasks.itemconfig(i, {
                    'bg': theme['listbox_bg'],
                    'fg': theme['listbox_fg']
                })
    
    def on_entry_focus_in(self, event):
        """Entry field focus in effect"""
        theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
        focus_color = "#455a64" if self.is_dark_theme else "#f8f9fa"
        self.entry_task.config(bg=focus_color)
    
    def on_entry_focus_out(self, event):
        """Entry field focus out effect"""
        theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
        self.entry_task.config(bg=theme['entry_bg'])
    
    def update_stats(self):
        """Updates the task statistics in header"""
        total_tasks = self.listbox_tasks.size()
        completed_tasks = 0
        theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
        
        for i in range(total_tasks):
            current_bg = self.listbox_tasks.itemcget(i, 'bg')
            if current_bg in [theme['completed_bg'], '#d5dbdb', '#566573']:
                completed_tasks += 1
        
        self.stats_label.config(text=f"Total: {total_tasks} | Completed: {completed_tasks}")
    
    def add_task(self):
        """
        Gets the task from the entry field and adds it to the listbox with timestamp.
        """
        task = self.entry_task.get().strip()
        if task != "":
            timestamp = datetime.datetime.now().strftime("%H:%M")
            formatted_task = f"• {task} ({timestamp})"
            self.listbox_tasks.insert(tk.END, formatted_task)
            self.entry_task.delete(0, tk.END)
            self.update_stats()
            
            # Add visual feedback
            self.root.after(100, lambda: self.listbox_tasks.see(tk.END))
        else:
            messagebox.showwarning("⚠️ Warning", "Please enter a task before adding!")
            self.entry_task.focus_set()

    def delete_task(self):
        """
        Deletes the currently selected task from the listbox with confirmation.
        """
        try:
            task_index = self.listbox_tasks.curselection()[0]
            task_text = self.listbox_tasks.get(task_index)
            
            if messagebox.askyesno("🗑️ Confirm Delete", f"Delete this task?\n\n{task_text}"):
                self.listbox_tasks.delete(task_index)
                self.update_stats()
        except IndexError:
            messagebox.showwarning("⚠️ Warning", "Please select a task to delete!")

    def mark_completed(self):
        """
        Marks the currently selected task as completed with visual feedback.
        """
        try:
            task_index = self.listbox_tasks.curselection()[0]
            current_bg = self.listbox_tasks.itemcget(task_index, 'bg')
            theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
            
            if current_bg in [theme['completed_bg'], '#d5dbdb', '#566573']:  # Already completed
                # Unmark as completed
                self.listbox_tasks.itemconfig(task_index, {
                    'bg': theme['listbox_bg'],
                    'fg': theme['listbox_fg']
                })
            else:
                # Mark as completed
                self.listbox_tasks.itemconfig(task_index, {
                    'bg': theme['completed_bg'],
                    'fg': theme['completed_fg']
                })
            
            self.update_stats()
        except IndexError:
            messagebox.showwarning("⚠️ Warning", "Please select a task to mark as completed!")
    
    def clear_completed(self):
        """
        Removes all completed tasks from the list.
        """
        completed_indices = []
        theme = self.themes['dark'] if self.is_dark_theme else self.themes['light']
        
        for i in range(self.listbox_tasks.size()):
            current_bg = self.listbox_tasks.itemcget(i, 'bg')
            if current_bg in [theme['completed_bg'], '#d5dbdb', '#566573']:
                completed_indices.append(i)
        
        if completed_indices:
            if messagebox.askyesno("🧹 Clear Completed", f"Remove {len(completed_indices)} completed task(s)?"):
                # Delete from highest index to lowest to avoid index shifting
                for index in reversed(completed_indices):
                    self.listbox_tasks.delete(index)
                self.update_stats()
        else:
            messagebox.showinfo("📝 Info", "No completed tasks to clear!")

# --- Main Execution ---

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

