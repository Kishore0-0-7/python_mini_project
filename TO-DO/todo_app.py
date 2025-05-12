import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.hover_color = kwargs.pop('hover_color', '#4a6572')
        self.original_color = kwargs.get('bg', '#344955')
        
        super().__init__(master, **kwargs)
        
        # Add rounded corners and modern styling
        self.config(relief=tk.FLAT, borderwidth=0, padx=10)
        
        # Bind hover events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.config(bg=self.hover_color)
    
    def on_leave(self, event):
        self.config(bg=self.original_color)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("650x550")
        self.root.minsize(600, 500)
        
        # Set app color scheme (more modern)
        self.bg_color = "#f5f5f5"  # Lighter background
        self.header_color = "#344955"  # Darker header
        self.btn_color = "#4a6572"  # Primary button color
        self.accent_color = "#f9aa33"  # Accent color
        self.btn_text_color = "white"
        
        # Priority colors (more subtle and modern)
        self.priority_colors = {
            "High": "#ffcdd2",    # Lighter red
            "Medium": "#fff9c4",   # Lighter yellow
            "Low": "#dcedc8"      # Lighter green
        }
        
        # Priority icons
        self.priority_icons = {
            "High": "! ",    
            "Medium": "● ",   
            "Low": "○ "      
        }
        
        # Task states
        self.completed_icon = "✓ "
        self.uncompleted_icon = "• "
        
        self.root.configure(bg=self.bg_color)
        
        # Apply a custom theme to ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TCombobox', fieldbackground=self.bg_color, background=self.bg_color)
        
        # Data storage
        self.tasks = []
        self.load_tasks()
        
        # Initialize status_var first
        self.status_var = tk.StringVar()
        self.status_var.set(f"Total Tasks: {len(self.tasks)}")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # App components
        self.create_header()
        self.create_task_entry()
        self.create_buttons()
        self.create_task_listbox()
        self.create_status_bar()
        
        # Bind Enter key to add_task
        self.root.bind('<Return>', lambda event: self.add_task())
        
        # Bind double-click to edit_task
        self.task_listbox.bind('<Double-1>', lambda event: self.edit_task())
        
        # Bind right-click to show context menu
        self.task_listbox.bind("<Button-3>", self.show_context_menu)
        
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.header_color, height=60)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="My Tasks", 
            font=("Helvetica", 18, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(self.main_frame, bg="#dddddd", height=2)
        shadow_frame.pack(fill=tk.X, pady=(0, 10))
        
    def create_task_entry(self):
        entry_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        entry_frame.pack(fill=tk.X, pady=10)
        
        # Task entry with placeholder
        self.task_entry = tk.Entry(
            entry_frame, 
            width=40, 
            font=("Helvetica", 12),
            bg="white",
            fg="#333333",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#dddddd",
            highlightcolor=self.accent_color
        )
        self.task_entry.pack(side=tk.LEFT, padx=5, ipady=8)
        
        # Add placeholder text
        self.task_entry.insert(0, "Add a new task...")
        self.task_entry.config(fg="#999999")
        
        # Bind focus events for placeholder behavior
        self.task_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.task_entry.bind("<FocusOut>", self.on_entry_focus_out)
        
        self.task_entry.focus()
        
        # Priority dropdown with styling
        priority_frame = tk.Frame(entry_frame, bg=self.bg_color)
        priority_frame.pack(side=tk.LEFT, padx=5)
        
        priority_label = tk.Label(
            priority_frame, 
            text="Priority:", 
            bg=self.bg_color,
            font=("Helvetica", 10)
        )
        priority_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")  # Default priority
        
        self.priority_dropdown = ttk.Combobox(
            priority_frame, 
            textvariable=self.priority_var, 
            values=["High", "Medium", "Low"],
            width=8,
            state="readonly"
        )
        self.priority_dropdown.pack(side=tk.LEFT, padx=5, ipady=3)
        
        # Style the add button
        add_button = ModernButton(
            entry_frame,
            text="Add Task",
            command=self.add_task,
            bg=self.btn_color,
            hover_color=self.accent_color,
            fg=self.btn_text_color,
            font=("Helvetica", 10, "bold"),
            width=10,
            cursor="hand2"
        )
        add_button.pack(side=tk.LEFT, padx=5, ipady=3)
    
    def create_buttons(self):
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Style all buttons with the ModernButton class
        complete_button = ModernButton(
            button_frame,
            text="Mark Complete",
            command=self.mark_complete,
            bg=self.btn_color,
            hover_color=self.accent_color,
            fg=self.btn_text_color,
            font=("Helvetica", 10),
            width=12,
            cursor="hand2"
        )
        complete_button.pack(side=tk.LEFT, padx=5, ipady=3)
        
        edit_button = ModernButton(
            button_frame,
            text="Edit Task",
            command=self.edit_task,
            bg=self.btn_color,
            hover_color=self.accent_color,
            fg=self.btn_text_color,
            font=("Helvetica", 10),
            width=10,
            cursor="hand2"
        )
        edit_button.pack(side=tk.LEFT, padx=5, ipady=3)
        
        delete_button = ModernButton(
            button_frame,
            text="Delete Task",
            command=self.delete_task,
            bg=self.btn_color,
            hover_color=self.accent_color,
            fg=self.btn_text_color,
            font=("Helvetica", 10),
            width=10,
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT, padx=5, ipady=3)
        
        clear_button = ModernButton(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            bg=self.btn_color,
            hover_color=self.accent_color,
            fg=self.btn_text_color,
            font=("Helvetica", 10),
            width=10,
            cursor="hand2"
        )
        clear_button.pack(side=tk.LEFT, padx=5, ipady=3)
        
        # Add filter option
        filter_frame = tk.Frame(button_frame, bg=self.bg_color)
        filter_frame.pack(side=tk.RIGHT, padx=5)
        
        filter_label = tk.Label(filter_frame, text="Filter:", bg=self.bg_color, font=("Helvetica", 10))
        filter_label.pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar()
        self.filter_var.set("All")
        
        filter_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Active", "Completed", "High Priority"],
            width=10,
            state="readonly"
        )
        filter_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Bind filter change event
        filter_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_listbox())
    
    def create_task_listbox(self):
        list_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add a heading
        listbox_label = tk.Label(
            list_frame, 
            text="Your Tasks", 
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            anchor=tk.W
        )
        listbox_label.pack(fill=tk.X, anchor=tk.W, pady=(0, 5))
        
        # Container for the listbox and scrollbar
        listbox_container = tk.Frame(list_frame, bg=self.bg_color, relief=tk.FLAT, bd=1, highlightbackground="#dddddd", highlightthickness=1)
        listbox_container.pack(fill=tk.BOTH, expand=True)
        
        self.task_listbox = tk.Listbox(
            listbox_container,
            font=("Helvetica", 11),
            selectbackground=self.accent_color,
            selectforeground="black",
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectmode=tk.SINGLE
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)
        
        self.update_listbox()
    
    def create_status_bar(self):
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            bg="#eeeeee",
            fg="#666666",
            bd=1,
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_entry_focus_in(self, event):
        if self.task_entry.get() == "Add a new task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg="#333333")
    
    def on_entry_focus_out(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, "Add a new task...")
            self.task_entry.config(fg="#999999")
    
    def show_context_menu(self, event):
        try:
            selected_index = self.task_listbox.nearest(event.y)
            if selected_index >= 0 and selected_index < len(self.tasks):
                self.task_listbox.selection_clear(0, tk.END)
                self.task_listbox.selection_set(selected_index)
                
                # Create popup menu
                popup_menu = tk.Menu(self.root, tearoff=0)
                
                popup_menu.add_command(label="Edit Task", command=self.edit_task)
                
                # Check completion status
                if self.tasks[selected_index]["completed"]:
                    popup_menu.add_command(label="Mark as Incomplete", command=self.mark_complete)
                else:
                    popup_menu.add_command(label="Mark as Complete", command=self.mark_complete)
                
                popup_menu.add_separator()
                
                # Priority submenu
                priority_menu = tk.Menu(popup_menu, tearoff=0)
                for priority in ["High", "Medium", "Low"]:
                    priority_menu.add_command(
                        label=priority,
                        command=lambda p=priority: self.change_priority(selected_index, p)
                    )
                popup_menu.add_cascade(label="Set Priority", menu=priority_menu)
                
                popup_menu.add_separator()
                popup_menu.add_command(label="Delete Task", command=self.delete_task)
                
                # Display menu
                popup_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass
    
    def change_priority(self, index, priority):
        self.tasks[index]["priority"] = priority
        self.update_listbox()
        self.save_tasks()
    
    def add_task(self):
        task = self.task_entry.get().strip()
        # Don't add task if it's the placeholder text
        if task == "Add a new task...":
            task = ""
            
        priority = self.priority_var.get()
        
        if task:
            self.tasks.append({
                "task": task, 
                "completed": False,
                "priority": priority,
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.update_listbox()
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, "Add a new task...")
            self.task_entry.config(fg="#999999")
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[selected_index]["task"]
            current_priority = self.tasks[selected_index]["priority"]
            
            # Create custom dialog with modern styling
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("450x220")
            edit_window.resizable(False, False)
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            # Set background color
            edit_window.configure(bg=self.bg_color)
            
            # Center the window
            edit_window.geometry("+%d+%d" % (
                self.root.winfo_rootx() + 50,
                self.root.winfo_rooty() + 50
            ))
            
            # Header
            header_label = tk.Label(
                edit_window,
                text="Edit Your Task",
                font=("Helvetica", 14, "bold"),
                bg=self.bg_color,
                fg="#333333"
            )
            header_label.pack(pady=(15, 20))
            
            # Entry with the current task
            edit_entry = tk.Entry(
                edit_window, 
                width=45, 
                font=("Helvetica", 12),
                bg="white",
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground="#dddddd",
                highlightcolor=self.accent_color
            )
            edit_entry.insert(0, current_task)
            edit_entry.pack(pady=5, padx=20, ipady=8)
            edit_entry.select_range(0, tk.END)
            edit_entry.focus()
            
            # Priority selection
            priority_frame = tk.Frame(edit_window, bg=self.bg_color)
            priority_frame.pack(pady=15)
            
            priority_label = tk.Label(
                priority_frame, 
                text="Priority:", 
                font=("Helvetica", 11),
                bg=self.bg_color
            )
            priority_label.pack(side=tk.LEFT, padx=5)
            
            priority_var = tk.StringVar()
            priority_var.set(current_priority)
            
            priority_dropdown = ttk.Combobox(
                priority_frame, 
                textvariable=priority_var, 
                values=["High", "Medium", "Low"],
                width=8,
                state="readonly"
            )
            priority_dropdown.pack(side=tk.LEFT, padx=5)
            
            # Button frame
            button_frame = tk.Frame(edit_window, bg=self.bg_color)
            button_frame.pack(pady=15)
            
            # Function to save changes
            def save_changes():
                new_task = edit_entry.get().strip()
                new_priority = priority_var.get()
                
                if new_task:
                    self.tasks[selected_index]["task"] = new_task
                    self.tasks[selected_index]["priority"] = new_priority
                    self.update_listbox()
                    self.save_tasks()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Task cannot be empty!")
            
            # Modern styled buttons
            save_button = ModernButton(
                button_frame, 
                text="Save Changes", 
                command=save_changes,
                bg=self.btn_color,
                hover_color=self.accent_color,
                fg=self.btn_text_color,
                width=12,
                cursor="hand2"
            )
            save_button.pack(side=tk.LEFT, padx=5, ipady=3)
            
            cancel_button = ModernButton(
                button_frame, 
                text="Cancel", 
                command=edit_window.destroy,
                bg="#999999",
                hover_color="#777777",
                fg="white",
                width=10,
                cursor="hand2"
            )
            cancel_button.pack(side=tk.LEFT, padx=5, ipady=3)
            
            # Bind Enter key to save changes
            edit_window.bind('<Return>', lambda event: save_changes())
            
            # Wait for this window to be destroyed before returning
            self.root.wait_window(edit_window)
            
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_to_delete = self.tasks[selected_index]["task"]
            
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete the task:\n\n{task_to_delete}?",
                icon="warning"
            )
            
            if confirm:
                del self.tasks[selected_index]
                self.update_listbox()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear.")
            return
            
        confirmed = messagebox.askyesno(
            "Confirmation", 
            f"Are you sure you want to delete all {len(self.tasks)} tasks?",
            icon="warning"
        )
        if confirmed:
            self.tasks = []
            self.update_listbox()
            self.save_tasks()
    
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        
        # Get the current filter
        current_filter = self.filter_var.get()
        
        # Filter tasks according to the selected filter
        filtered_tasks = []
        for task in self.tasks:
            if current_filter == "All":
                filtered_tasks.append(task)
            elif current_filter == "Active" and not task["completed"]:
                filtered_tasks.append(task)
            elif current_filter == "Completed" and task["completed"]:
                filtered_tasks.append(task)
            elif current_filter == "High Priority" and task["priority"] == "High":
                filtered_tasks.append(task)
        
        # Sort tasks by priority (High > Medium > Low) and completion status
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        sorted_tasks = sorted(filtered_tasks, 
                             key=lambda x: (x["completed"], 
                                           priority_order.get(x.get("priority", "Medium"), 1)))
        
        # Display tasks in the listbox
        for task in sorted_tasks:
            task_text = task["task"]
            priority = task.get("priority", "Medium")
            
            # Add priority icon and completion status
            if task["completed"]:
                prefix = self.completed_icon
            else:
                prefix = self.uncompleted_icon
                
            # Add priority indicator
            priority_prefix = self.priority_icons.get(priority, "● ")
            
            # Combine all prefixes
            final_prefix = f"{priority_prefix}"
            
            # Format the task display
            task_text = f"{final_prefix}{task_text}"
            if task["completed"]:
                task_text = f"✓ {task_text}"
            
            self.task_listbox.insert(tk.END, task_text)
            
            # Color the task based on priority and completion
            last_index = self.task_listbox.size() - 1
            
            if task["completed"]:
                # Gray out completed tasks
                self.task_listbox.itemconfig(
                    last_index,
                    fg="#999999",
                    bg="#f9f9f9"
                )
            else:
                # Color according to priority
                self.task_listbox.itemconfig(
                    last_index,
                    bg=self.priority_colors.get(priority, self.bg_color)
                )
        
        # Update status bar
        completed_count = sum(1 for task in self.tasks if task["completed"])
        active_count = len(self.tasks) - completed_count
        high_priority_count = sum(1 for task in self.tasks if task.get("priority") == "High" and not task["completed"])
        
        self.status_var.set(
            f"Total: {len(self.tasks)} | "
            f"Active: {active_count} | "
            f"Completed: {completed_count} | "
            f"High Priority: {high_priority_count}"
        )
    
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                
                # Ensure all tasks have required fields
                for task in self.tasks:
                    if "priority" not in task:
                        task["priority"] = "Medium"
                    if "date_added" not in task:
                        task["date_added"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop() 