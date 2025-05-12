import tkinter as tk
from tkinter import ttk, messagebox
import math
import re
from typing import Optional

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, padding=0, color="#e1e1e1", text="", text_color="black", 
                 text_font=("Helvetica", 14), command=None, hover_color=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.color = color
        self.hover_color = hover_color if hover_color else self._get_hover_color(color)
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.command = command
        self.is_clicked = False

        # Draw shadow first (slightly larger, offset rect with darker color)
        shadow_color = self._get_shadow_color(color)
        self.shadow = self.create_rounded_rect(padding+2, padding+2, width-padding+2, height-padding+2, 
                                             corner_radius, fill=shadow_color, outline="")
        
        # Draw rounded rectangle
        self.rect = self.create_rounded_rect(padding, padding, width-padding, height-padding, 
                                           corner_radius, fill=color, outline="")
        
        # Add text
        self.text_id = self.create_text(width/2, height/2, text=text, fill=text_color, font=text_font)
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _get_hover_color(self, hex_color):
        # Make color lighter for hover effect
        r = min(255, int(int(hex_color[1:3], 16) * 1.1))
        g = min(255, int(int(hex_color[3:5], 16) * 1.1))
        b = min(255, int(int(hex_color[5:7], 16) * 1.1))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _get_shadow_color(self, hex_color):
        # Make color darker for shadow effect
        r = max(0, int(int(hex_color[1:3], 16) * 0.7))
        g = max(0, int(int(hex_color[3:5], 16) * 0.7))
        b = max(0, int(int(hex_color[5:7], 16) * 0.7))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        # Create rounded rectangle
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
    
    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color)
        self.is_clicked = False
    
    def _on_press(self, event):
        self.is_clicked = True
        # Create a darker color for pressing effect
        r = max(0, int(int(self.color[1:3], 16) * 0.9))
        g = max(0, int(int(self.color[3:5], 16) * 0.9))
        b = max(0, int(int(self.color[5:7], 16) * 0.9))
        pressed_color = f"#{r:02x}{g:02x}{b:02x}"
        self.itemconfig(self.rect, fill=pressed_color)
        
        # Move shadow for 3D press effect
        self.itemconfig(self.shadow, fill=pressed_color)
        self.coords(self.shadow, self.coords(self.rect))
    
    def _on_release(self, event):
        if self.is_clicked and self.command:
            # Call the command only if we're still over the button
            if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height():
                self.command()
                
        # Reset the button appearance
        self.itemconfig(self.rect, fill=self.hover_color)
        shadow_color = self._get_shadow_color(self.hover_color)
        self.itemconfig(self.shadow, fill=shadow_color)
        
        # Reset shadow position
        shadow_coords = self.coords(self.rect)
        new_shadow_coords = []
        for i in range(0, len(shadow_coords), 2):
            new_shadow_coords.append(shadow_coords[i] + 2)
            new_shadow_coords.append(shadow_coords[i+1] + 2)
        self.coords(self.shadow, *new_shadow_coords)
        
        self.is_clicked = False

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("420x620")  # Slightly larger window
        self.root.resizable(False, False)
        self.root.configure(background="#f0f2f5")  # Set a consistent background
        
        # Set app color scheme with more vibrant colors
        self.bg_color = "#f0f2f5"  # Lighter background
        self.primary_color = "#1a2a3a"  # Darker blue/gray
        self.accent_color = "#ff5252"  # Vibrant red
        self.secondary_color = "#4caf50"  # Vibrant green
        self.bracket_color = "#2196f3"  # Brighter blue for brackets
        
        self.number_btn_color = "#ffffff"  # White
        self.op_btn_color = "#e9ecef"  # Light gray
        self.eq_btn_color = self.accent_color
        self.clear_btn_color = self.primary_color
        self.func_btn_color = "#9c27b0"  # Brighter purple for functions
        
        # Set the window icon (if supported by the platform)
        try:
            self.root.iconbitmap("calculator.ico")
        except:
            pass  # Icon not available, just continue
        
        # Cursor position and selection variables
        self.cursor_position = 0
        
        # Expression to calculate
        self.expression = ""
        self.history = []
        self.bracket_count = 0
        
        # Create main frames
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the display and buttons
        self.create_display()
        self.create_history_display()
        self.create_buttons()
        
        # Add some shadows and effects
        self.add_visual_effects()
        
        # Create scientific calculator elements
        self.scientific_mode = False
        self.scientific_frame = None
        self.toggle_scientific_button()
        
        # Add keyboard bindings
        self.add_keyboard_bindings()
    
    def add_keyboard_bindings(self):
        # Numbers and operations
        for key in "0123456789+-*/().%":
            self.root.bind(key, lambda event, k=key: self.key_pressed(k))
        
        # Enter for equals
        self.root.bind("<Return>", lambda event: self.calculate())
        
        # Backspace for delete
        self.root.bind("<BackSpace>", lambda event: self.backspace_pressed())
        
        # Delete key
        self.root.bind("<Delete>", lambda event: self.delete_at_cursor())
        
        # Left and right arrow keys for cursor movement
        self.root.bind("<Left>", lambda event: self.move_cursor(-1))
        self.root.bind("<Right>", lambda event: self.move_cursor(1))
        
        # Home and End keys
        self.root.bind("<Home>", lambda event: self.cursor_to_start())
        self.root.bind("<End>", lambda event: self.cursor_to_end())
        
        # Escape for clear
        self.root.bind("<Escape>", lambda event: self.clear())
    
    def key_pressed(self, key):
        if key == '=':
            self.calculate()
        else:
            self.insert_at_cursor(key)
    
    def move_cursor(self, delta):
        new_position = self.cursor_position + delta
        if 0 <= new_position <= len(self.expression):
            self.cursor_position = new_position
            self.display.icursor(self.cursor_position)
    
    def cursor_to_start(self):
        self.cursor_position = 0
        self.display.icursor(0)
    
    def cursor_to_end(self):
        self.cursor_position = len(self.expression)
        self.display.icursor(len(self.expression))
    
    def backspace_pressed(self):
        if self.cursor_position > 0 and len(self.expression) > 0:
            # Get character to delete
            char_to_delete = None
            if self.cursor_position > 0 and self.cursor_position <= len(self.expression):
                char_to_delete = self.expression[self.cursor_position-1]
            
            # Delete character before cursor
            before_cursor = self.expression[:self.cursor_position-1]
            after_cursor = self.expression[self.cursor_position:]
            self.expression = before_cursor + after_cursor
            
            # Update bracket count if needed
            if char_to_delete == "(":
                self.bracket_count = max(0, self.bracket_count - 1)
            elif char_to_delete == ")":
                self.bracket_count += 1
            
            self.expression_var.set(self.expression)
            self.cursor_position -= 1
            self.display.icursor(self.cursor_position)
            self.update_result()
            self.update_bracket_indicator()
    
    def delete_at_cursor(self):
        if self.cursor_position < len(self.expression):
            # Get character to delete
            char_to_delete = None
            if self.cursor_position < len(self.expression):
                char_to_delete = self.expression[self.cursor_position]
            
            # Delete character at cursor
            before_cursor = self.expression[:self.cursor_position]
            after_cursor = self.expression[self.cursor_position+1:]
            
            # Update bracket count if needed
            if char_to_delete == "(":
                self.bracket_count = max(0, self.bracket_count - 1)
            elif char_to_delete == ")":
                self.bracket_count += 1
            
            self.expression = before_cursor + after_cursor
            self.expression_var.set(self.expression)
            self.display.icursor(self.cursor_position)
            self.update_result()
            self.update_bracket_indicator()
    
    def add_visual_effects(self):
        # Add app name at bottom
        app_name = tk.Label(
            self.root,
            text="Advanced Scientific Calculator",
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color,
            fg="#777777"
        )
        app_name.pack(side=tk.BOTTOM, pady=5)
    
    def create_display(self):
        # Main display area with rounded corners
        display_frame = tk.Frame(self.main_frame, bg=self.bg_color, padx=5, pady=5)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a border frame with a raised effect for the display
        border_frame = tk.Frame(display_frame, bg="white", bd=2, relief=tk.RAISED)
        border_frame.pack(fill=tk.X, pady=5)
        
        # Expression entry with stylish font - now editable
        self.expression_var = tk.StringVar()
        
        # Create a label frame for better spacing and alignment
        entry_frame = tk.Frame(border_frame, bg="white", padx=10, pady=10)
        entry_frame.pack(fill=tk.X)
        
        self.display = tk.Entry(
            entry_frame,
            textvariable=self.expression_var,
            font=("Helvetica", 24),
            bd=0,
            justify=tk.RIGHT,
            bg="white",
            fg=self.primary_color,
            highlightthickness=0,
            insertbackground=self.accent_color,  # Cursor color
            insertwidth=2  # Cursor width
        )
        self.display.pack(fill=tk.X, ipady=15)
        
        # Instead of making it read-only, we'll intercept key events
        self.display.bind("<Key>", self.handle_display_key)
        
        # When the entry gets focus, update cursor position
        self.display.bind("<FocusIn>", self.update_cursor_position)
        self.display.bind("<Button-1>", self.update_cursor_position)
        
        # Info container frame
        info_frame = tk.Frame(border_frame, bg="white", padx=10, pady=5)
        info_frame.pack(fill=tk.X)
        
        # Bracket balance indicator
        self.bracket_indicator = tk.Label(
            info_frame,
            text="✓ Brackets: balanced",
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg="green",
            anchor=tk.W
        )
        self.bracket_indicator.pack(side=tk.LEFT, fill=tk.X)
        
        # Cursor position indicator
        self.cursor_position_label = tk.Label(
            info_frame,
            text="Cursor: 0",
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg=self.primary_color,
            anchor=tk.E
        )
        self.cursor_position_label.pack(side=tk.RIGHT, fill=tk.X)
        
        # Result label with bigger font
        result_frame = tk.Frame(border_frame, bg="white", padx=10, pady=10)
        result_frame.pack(fill=tk.X)
        
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        result_label = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Helvetica", 36, "bold"),
            bg="white",
            fg=self.primary_color,
            anchor=tk.E
        )
        result_label.pack(fill=tk.X)
    
    def handle_display_key(self, event):
        # Allow only specific keys - intercept all others
        allowed_chars = "0123456789+-*/().%^e "
        
        # Allow cursor movement and editing keys
        if event.keysym in ("Left", "Right", "Home", "End", "BackSpace", "Delete", "Return", "Escape"):
            return  # Let these keys pass through
        
        # Allow control keys for copy/paste
        if event.state & 4:  # Control key is pressed
            if event.keysym in ("c", "v", "x", "a"):
                return  # Allow copy/paste/cut/select all
        
        # For regular characters, check if allowed
        if event.char and event.char in allowed_chars:
            # Update cursor position before character is inserted
            self.update_cursor_position(event)
            # Let it pass through
            return
            
        # Block all other keys
        return "break"
    
    def update_cursor_position(self, event=None):
        # Update cursor position after a short delay to ensure it's accurate
        self.root.after(10, self._update_cursor)
    
    def _update_cursor(self):
        try:
            self.cursor_position = self.display.index(tk.INSERT)
            self.cursor_position_label.config(text=f"Cursor: {self.cursor_position}")
            # Get the latest expression from the entry
            self.expression = self.expression_var.get()
            self.update_result()
        except:
            pass
    
    def insert_at_cursor(self, text):
        try:
            # Insert text at the current cursor position
            before_cursor = self.expression[:self.cursor_position]
            after_cursor = self.expression[self.cursor_position:]
            
            # Special handling for multiplication by 0
            if text == '0' and len(before_cursor) > 0 and before_cursor[-1] == '*' and not after_cursor:
                # Don't process further - just insert the 0
                pass
            # Special case for handling parentheses
            elif text == '(' and len(before_cursor) > 0:
                # Add implicit multiplication before ( if needed
                prev_char = before_cursor[-1]
                if prev_char.isdigit() or prev_char in ')πe':
                    text = "*" + text
            
            # Update bracket count if needed
            if text == "(":
                self.bracket_count += 1
            elif text == ")":
                if self.bracket_count > 0:
                    self.bracket_count -= 1
                else:
                    # Don't add a closing bracket if there's no opening bracket
                    return
            
            # Update the expression
            self.expression = before_cursor + text + after_cursor
            self.expression_var.set(self.expression)
            
            # Update cursor position
            new_cursor_position = self.cursor_position + len(text)
            self.cursor_position = new_cursor_position
            self.display.icursor(new_cursor_position)
            
            # Update calculations and display
            self.update_result()
            self.update_bracket_indicator()
        except Exception as e:
            print(f"Insert error: {str(e)}")
            # If any error occurs, ensure we don't break the calculator
            self.result_var.set("Input Error")
    
    def create_history_display(self):
        # History section with a border
        history_frame = tk.Frame(self.main_frame, bg=self.bg_color, bd=1, relief=tk.SOLID)
        history_frame.pack(fill=tk.X, padx=15, pady=12)
        
        history_header = tk.Frame(history_frame, bg=self.primary_color)
        history_header.pack(fill=tk.X)
        
        history_label = tk.Label(
            history_header,
            text=" History",
            font=("Helvetica", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            anchor=tk.W,
            padx=5,
            pady=2
        )
        history_label.pack(side=tk.LEFT, anchor=tk.W)
        
        self.history_var = tk.StringVar()
        self.history_display = tk.Label(
            history_frame,
            textvariable=self.history_var,
            font=("Helvetica", 10),
            bg="white",
            fg="#555555",
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=380,
            padx=10,
            pady=5
        )
        self.history_display.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
    
    def create_buttons(self):
        # Main buttons area
        main_buttons_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        main_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configure the grid
        for i in range(6):
            main_buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            main_buttons_frame.columnconfigure(i, weight=1)
        
        # Special function buttons row
        self.create_special_buttons(main_buttons_frame)
        
        # Regular calculator buttons
        self.create_calculator_buttons(main_buttons_frame)
    
    def create_special_buttons(self, parent_frame):
        # Row for special buttons
        special_buttons = [
            ("C", 0, 0, self.clear_btn_color, "white"),
            ("DEL", 0, 1, self.clear_btn_color, "white"),
            ("±", 0, 2, self.op_btn_color, self.primary_color),
            ("/", 0, 3, self.op_btn_color, self.primary_color)
        ]
        
        for btn_info in special_buttons:
            text, row, col, bg_color, fg_color = btn_info
            btn = RoundedButton(
                parent_frame,
                width=85,
                height=65,
                corner_radius=12,
                padding=2,
                color=bg_color,
                text=text,
                text_color=fg_color,
                text_font=("Helvetica", 16, "bold" if text in ["=", "C"] else "normal"),
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
    
    def create_calculator_buttons(self, parent_frame):
        # Regular calculator buttons
        calculator_buttons = [
            ("7", 1, 0, self.number_btn_color, self.primary_color),
            ("8", 1, 1, self.number_btn_color, self.primary_color),
            ("9", 1, 2, self.number_btn_color, self.primary_color),
            ("*", 1, 3, self.op_btn_color, self.primary_color),
            
            ("4", 2, 0, self.number_btn_color, self.primary_color),
            ("5", 2, 1, self.number_btn_color, self.primary_color),
            ("6", 2, 2, self.number_btn_color, self.primary_color),
            ("-", 2, 3, self.op_btn_color, self.primary_color),
            
            ("1", 3, 0, self.number_btn_color, self.primary_color),
            ("2", 3, 1, self.number_btn_color, self.primary_color),
            ("3", 3, 2, self.number_btn_color, self.primary_color),
            ("+", 3, 3, self.op_btn_color, self.primary_color),
            
            ("0", 4, 0, self.number_btn_color, self.primary_color),
            (".", 4, 1, self.number_btn_color, self.primary_color),
            ("%", 4, 2, self.op_btn_color, self.primary_color)
        ]
        
        for btn_info in calculator_buttons:
            text, row, col, bg_color, fg_color = btn_info
            btn = RoundedButton(
                parent_frame,
                width=85,
                height=65,
                corner_radius=12,
                padding=2,
                color=bg_color,
                text=text,
                text_color=fg_color,
                text_font=("Helvetica", 18),
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        
        # Equal button (spans two columns)
        equal_btn = RoundedButton(
            parent_frame,
            width=175,
            height=65,
            corner_radius=12,
            padding=2,
            color=self.eq_btn_color,
            text="=",
            text_color="white",
            text_font=("Helvetica", 24, "bold"),
            command=lambda: self.button_click("=")
        )
        equal_btn.grid(row=4, column=3, padx=4, pady=4, sticky="nsew")
        
        # Add bracket buttons
        brackets_frame = tk.Frame(parent_frame, bg=self.bg_color)
        brackets_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Configure the grid for brackets frame
        brackets_frame.columnconfigure(0, weight=1)
        brackets_frame.columnconfigure(1, weight=1)
        brackets_frame.rowconfigure(0, weight=1)
        
        # Left bracket
        left_bracket_btn = RoundedButton(
            brackets_frame,
            width=80,
            height=60,
            corner_radius=10,
            padding=2,
            color=self.bracket_color,
            text="(",
            text_color="white",
            text_font=("Helvetica", 18, "bold"),
            command=lambda: self.button_click("(")
        )
        left_bracket_btn.grid(row=0, column=0, padx=3, pady=0, sticky="nsew")
        
        # Right bracket
        right_bracket_btn = RoundedButton(
            brackets_frame,
            width=80,
            height=60,
            corner_radius=10,
            padding=2,
            color=self.bracket_color,
            text=")",
            text_color="white",
            text_font=("Helvetica", 18, "bold"),
            command=lambda: self.button_click(")")
        )
        right_bracket_btn.grid(row=0, column=1, padx=3, pady=0, sticky="nsew")
        
        # Scientific mode toggle button
        sci_btn = RoundedButton(
            parent_frame,
            width=170,
            height=60,
            corner_radius=10,
            padding=2,
            color=self.secondary_color,
            text="↔ Scientific",
            text_color="white",
            text_font=("Helvetica", 16, "bold"),
            command=self.toggle_scientific_mode
        )
        sci_btn.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        
        if self.scientific_mode:
            if not self.scientific_frame:
                self.create_scientific_buttons()
            self.scientific_frame.pack(fill=tk.X, padx=20, pady=10)
            self.root.geometry("420x790")  # Make window taller
            if hasattr(self, 'sci_indicator'):
                self.sci_indicator.config(text="✓ Scientific Mode Active")
                self.sci_indicator.pack(side=tk.BOTTOM, pady=2)
        else:
            if self.scientific_frame:
                self.scientific_frame.pack_forget()
            self.root.geometry("420x620")  # Return to original size
            if hasattr(self, 'sci_indicator'):
                self.sci_indicator.config(text="✗ Scientific Mode Inactive")
                self.sci_indicator.pack(side=tk.BOTTOM, pady=2)
    
    def create_scientific_buttons(self):
        self.scientific_frame = tk.Frame(self.root, bg=self.bg_color)
        
        # Configure the grid for scientific buttons
        for i in range(4):
            self.scientific_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.scientific_frame.columnconfigure(i, weight=1)
        
        # Define all scientific buttons in rows with their colors
        scientific_buttons = [
            # Row 1
            ("sin", 0, 0, self.secondary_color, "white"),
            ("cos", 0, 1, self.secondary_color, "white"),
            ("tan", 0, 2, self.secondary_color, "white"),
            ("√", 0, 3, self.secondary_color, "white"),
            
            # Row 2
            ("log₁₀", 1, 0, self.secondary_color, "white"),
            ("ln", 1, 1, self.secondary_color, "white"),
            ("π", 1, 2, self.secondary_color, "white"),
            ("^", 1, 3, self.secondary_color, "white"),
            
            # Row 3
            ("asin", 2, 0, self.func_btn_color, "white"),
            ("acos", 2, 1, self.func_btn_color, "white"),
            ("atan", 2, 2, self.func_btn_color, "white"),
            ("e", 2, 3, self.secondary_color, "white"),
            
            # Row 4
            ("x²", 3, 0, self.func_btn_color, "white"),
            ("x³", 3, 1, self.func_btn_color, "white"),
            ("1/x", 3, 2, self.func_btn_color, "white"),
            ("abs", 3, 3, self.secondary_color, "white"),
        ]
        
        # Create the scientific buttons
        for btn_info in scientific_buttons:
            text, row, col, bg_color, fg_color = btn_info
            btn = RoundedButton(
                self.scientific_frame,
                width=80,
                height=60,
                corner_radius=10,
                padding=2,
                color=bg_color,
                text=text,
                text_color=fg_color,
                text_font=("Helvetica", 14),
                command=lambda t=text: self.scientific_button_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    def scientific_button_click(self, text):
        try:
            if text == "sin":
                self.insert_at_cursor("sin(")
                self.bracket_count += 1
            elif text == "cos":
                self.insert_at_cursor("cos(")
                self.bracket_count += 1
            elif text == "tan":
                self.insert_at_cursor("tan(")
                self.bracket_count += 1
            elif text == "asin":
                self.insert_at_cursor("asin(")
                self.bracket_count += 1
            elif text == "acos":
                self.insert_at_cursor("acos(")
                self.bracket_count += 1
            elif text == "atan":
                self.insert_at_cursor("atan(")
                self.bracket_count += 1
            elif text == "log₁₀":
                self.insert_at_cursor("log10(")
                self.bracket_count += 1
            elif text == "ln":
                self.insert_at_cursor("ln(")
                self.bracket_count += 1
            elif text == "√":
                self.insert_at_cursor("sqrt(")
                self.bracket_count += 1
            elif text == "^":
                self.insert_at_cursor("^")
            elif text == "π":
                self.insert_at_cursor("π")
            elif text == "e":
                self.insert_at_cursor("e")
            elif text == "x²":
                # Check if there's a number or closing bracket at cursor position
                if self.cursor_position > 0 and len(self.expression) > 0:
                    if self.cursor_position <= len(self.expression):
                        char_before = self.expression[self.cursor_position-1]
                        if char_before.isdigit() or char_before == ')' or char_before in 'πe':
                            self.insert_at_cursor("^2")
                    else:
                        # If cursor is at the end, check the last character
                        if len(self.expression) > 0:
                            char_before = self.expression[-1]
                            if char_before.isdigit() or char_before == ')' or char_before in 'πe':
                                self.insert_at_cursor("^2")
            elif text == "x³":
                # Check if there's a number or closing bracket at cursor position
                if self.cursor_position > 0 and len(self.expression) > 0:
                    if self.cursor_position <= len(self.expression):
                        char_before = self.expression[self.cursor_position-1]
                        if char_before.isdigit() or char_before == ')' or char_before in 'πe':
                            self.insert_at_cursor("^3")
                    else:
                        # If cursor is at the end, check the last character
                        if len(self.expression) > 0:
                            char_before = self.expression[-1]
                            if char_before.isdigit() or char_before == ')' or char_before in 'πe':
                                self.insert_at_cursor("^3")
            elif text == "1/x":
                # Get the current selection if any
                try:
                    sel_start = self.display.index(tk.SEL_FIRST)
                    sel_end = self.display.index(tk.SEL_LAST)
                    selected_text = self.expression[sel_start:sel_end]
                    
                    # Replace the selection with 1/(selection)
                    before_sel = self.expression[:sel_start]
                    after_sel = self.expression[sel_end:]
                    self.expression = f"{before_sel}1/({selected_text}){after_sel}"
                    self.expression_var.set(self.expression)
                    
                    # Update cursor position
                    new_cursor_pos = sel_start + len(f"1/({selected_text})")
                    self.cursor_position = new_cursor_pos
                    self.display.icursor(new_cursor_pos)
                    
                    # Update bracket count
                    self.bracket_count += 1
                except:
                    # No selection, insert at cursor position
                    self.insert_at_cursor("1/(")
                    self.bracket_count += 1
            elif text == "abs":
                self.insert_at_cursor("abs(")
                self.bracket_count += 1
            
            self.update_result()
            self.update_bracket_indicator()
            self.update_cursor_position()
        except Exception as e:
            print(f"Scientific button error: {str(e)}")
            # If any error occurs, ensure we don't break the calculator
            self.result_var.set("Function Error")
    
    def toggle_scientific_button(self):
        # Add a small scientific mode indicator
        self.sci_indicator = tk.Label(
            self.root, 
            text="✗ Scientific Mode Inactive", 
            font=("Helvetica", 9, "bold"),
            bg=self.bg_color, 
            fg=self.secondary_color
        )
        self.sci_indicator.pack(side=tk.BOTTOM, pady=2)
    
    def button_click(self, text):
        try:
            if text == "=":
                self.calculate()
            elif text == "C":
                self.clear()
            elif text == "DEL":
                self.backspace_pressed()
            elif text == "±":
                self.negate_number()
            elif text == "(":
                self.insert_at_cursor("(")
            elif text == ")":
                self.insert_at_cursor(")")
            else:
                self.insert_at_cursor(text)
        except Exception as e:
            # Handle any unexpected errors during button clicks
            self.result_var.set("Error")
            print(f"Button click error: {str(e)}")
    
    def clear(self):
        # Clear the expression
        self.expression = ""
        self.expression_var.set("")
        self.result_var.set("0")
        self.bracket_count = 0
        self.update_bracket_indicator()
        
        # Reset cursor position
        self.cursor_position = 0
        self.display.icursor(0)
        self.update_cursor_position()
    
    def negate_number(self):
        # Toggle between positive and negative for the current number or expression
        if not self.expression:
            self.insert_at_cursor("-")
            return
        
        # Check if cursor is within a number
        before_cursor = self.expression[:self.cursor_position]
        after_cursor = self.expression[self.cursor_position:]
        
        # Find the number at or before the cursor position
        number_pattern = r'(^|[^\d.])(-?\d+\.?\d*|-?\d*\.?\d+)$'
        match_before = re.search(number_pattern, before_cursor)
        
        if match_before:
            # Get the matched number and its position
            prefix = match_before.group(1) if match_before.group(1) else ""
            number = match_before.group(2)
            start_pos = len(before_cursor) - len(number)
            
            # Negate the number
            if number.startswith('-'):
                negated_number = number[1:]  # Remove the minus sign
            else:
                negated_number = '-' + number  # Add a minus sign
            
            # Replace the number in the expression
            self.expression = before_cursor[:start_pos] + negated_number + after_cursor
            self.expression_var.set(self.expression)
            
            # Update cursor position to end of negated number
            new_cursor_pos = start_pos + len(negated_number)
            self.cursor_position = new_cursor_pos
            self.display.icursor(new_cursor_pos)
            
            self.update_result()
        elif self.cursor_position == 0:
            # If cursor is at the start, negate the entire expression
            self.expression = "-" + self.expression
            self.expression_var.set(self.expression)
            self.cursor_position += 1
            self.display.icursor(self.cursor_position)
            self.update_result()
        elif self.cursor_position == len(self.expression) and self.expression.endswith(")"):
            # If cursor is at the end after a closing bracket, negate the entire expression
            self.expression = "-(" + self.expression + ")"
            self.expression_var.set(self.expression)
            self.bracket_count += 1
            self.cursor_position = len(self.expression)
            self.display.icursor(self.cursor_position)
            self.update_bracket_indicator()
            self.update_result()
        else:
            # Otherwise, just insert a negative sign at cursor
            self.insert_at_cursor("-")
    
    def update_bracket_indicator(self):
        # Recalculate bracket count to ensure accuracy
        open_count = self.expression.count('(')
        close_count = self.expression.count(')')
        self.bracket_count = open_count - close_count
        
        if self.bracket_count == 0:
            self.bracket_indicator.config(
                text="✓ Brackets: balanced",
                fg="green"
            )
        else:
            # Display both count and a visual indicator of missing brackets
            bracket_text = f"⚠ Brackets: {open_count}({close_count})"
            self.bracket_indicator.config(
                text=bracket_text,
                fg="red"
            )
        
        # Update the cursor position indicator
        self.cursor_position_label.config(
            text=f"Cursor: {self.cursor_position}"
        )
    
    def update_result(self):
        if not self.expression:
            self.result_var.set("0")
            return
        
        try:
            # Recalculate bracket count to ensure accuracy
            open_count = self.expression.count('(')
            close_count = self.expression.count(')')
            self.bracket_count = open_count - close_count
            
            # First check if the expression is incomplete (has unclosed brackets)
            if self.bracket_count > 0:
                temp_expr = self.expression
                # Add temporary closing brackets for preview
                temp_expr += ")" * self.bracket_count
                
                # Try evaluating the completed expression
                try:
                    processed_expr = self.preprocess_expression(temp_expr)
                    result = self.safe_eval(processed_expr)
                    
                    # Format the result and show it's a preview
                    if isinstance(result, float):
                        if abs(result - round(result)) < 1e-10:
                            formatted_result = str(int(round(result)))
                        else:
                            formatted_result = f"{result:.8f}".rstrip("0").rstrip(".")
                    else:
                        formatted_result = str(result)
                    
                    # Display the result (without Preview: prefix)
                    self.result_var.set(formatted_result)
                    return
                except Exception as e:
                    error_msg = str(e)
                    if "division by zero" in error_msg.lower():
                        self.result_var.set("Cannot divide by zero")
                    elif "invalid syntax" in error_msg.lower():
                        self.result_var.set("Syntax Error")
                    else:
                        # If the preview calculation fails for other reasons, show brackets needed
                        self.result_var.set(f"Add {self.bracket_count} bracket(s)")
                    return
                
            # For complete expressions (no unclosed brackets)
            processed_expr = self.preprocess_expression(self.expression)
            result = self.safe_eval(processed_expr)
            
            # Format the result
            if isinstance(result, float):
                if abs(result - round(result)) < 1e-10:
                    formatted_result = str(int(round(result)))
                else:
                    formatted_result = f"{result:.8f}".rstrip("0").rstrip(".")
            else:
                formatted_result = str(result)
            
            self.result_var.set(formatted_result)
            
        except Exception as e:
            error_msg = str(e)
            # Handle different types of errors
            if "never closed" in error_msg or "unexpected EOF" in error_msg:
                self.result_var.set(f"Add {self.bracket_count} bracket(s)")
            elif "division by zero" in error_msg.lower():
                self.result_var.set("Cannot divide by zero")
            elif "invalid syntax" in error_msg.lower():
                self.result_var.set("Syntax Error")
            else:
                # For other errors, show a clearer message when possible
                error_type = error_msg.split(':')[0] if ':' in error_msg else "Error"
                self.result_var.set(error_type)
                print(f"Calculation error: {error_msg}")
    
    def preprocess_expression(self, expr):
        """Process the expression to handle implicit multiplication and other preprocessing."""
        try:
            # Replace scientific notation e notation with proper Python syntax
            expr = re.sub(r'(\d+)e(\d+)', r'\1*10**\2', expr)
            
            # Handle implicit multiplication carefully:
            
            # Handle direct number * parenthesis: 10*(5 - ensure it's valid for calculation
            expr = re.sub(r'(\d+)\*\(', r'\1*(', expr)
            
            # Case 1: number followed by open bracket: 5(3+2) => 5*(3+2)
            expr = re.sub(r'(\d+|\))(\()', r'\1*\2', expr)
            
            # Case 2: number followed by pi or e: 2π => 2*π, 3e => 3*e
            expr = re.sub(r'(\d+)([πe])', r'\1*\2', expr)
            
            # Case 3: closing bracket followed by number: (3+2)5 => (3+2)*5
            expr = re.sub(r'(\))(\d+)', r'\1*\2', expr)
            
            # Case 4: closing bracket followed by letter or pi: (3+2)e => (3+2)*e, (3+2)π => (3+2)*π
            expr = re.sub(r'(\))([πe])', r'\1*\2', expr)
            
            # Handle π and e constants
            expr = expr.replace('π', 'math.pi').replace('e', 'math.e')
            
            # Replace ^ with ** for exponentiation
            expr = expr.replace('^', '**')
            
            # Replace × and ÷ with * and /
            expr = expr.replace('×', '*').replace('÷', '/')
            
            # Final check to make sure expression is valid for calculation
            # If there are still unclosed parentheses, add them
            open_count = expr.count('(')
            close_count = expr.count(')')
            if open_count > close_count:
                expr += ')' * (open_count - close_count)
            
            return expr
        except Exception as e:
            print(f"Error preprocessing expression: {str(e)}")
            return expr  # Return original if error
    
    def safe_eval(self, expr):
        """Safely evaluate a mathematical expression."""
        try:
            # Basic syntax check before evaluation
            if not expr or expr.isspace():
                return 0
            
            # Check for unbalanced brackets
            open_brackets = expr.count('(')
            close_brackets = expr.count(')')
            
            if open_brackets != close_brackets:
                if open_brackets > close_brackets:
                    missing = open_brackets - close_brackets
                    raise ValueError(f"Missing {missing} closing bracket(s)")
                else:
                    extra = close_brackets - open_brackets
                    raise ValueError(f"Extra {extra} closing bracket(s)")
                
            # Check for syntax errors that would cause eval to fail
            # Common cases like empty parentheses, consecutive operators, etc.
            if '()' in expr:
                raise ValueError("Empty parentheses")
            
            # Multiple consecutive operators are usually errors (like +*/ or */+)
            if re.search(r'[\+\-\*\/]{2,}', expr):
                raise ValueError("Invalid operator sequence")
            
            # Define safe functions and constants
            safe_dict = {
                'abs': abs,
                'math': math,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e
            }
            
            # Try the evaluation
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            
            # Don't return complex numbers from calculator
            if isinstance(result, complex):
                raise ValueError("Result is a complex number")
            
            return result
            
        except Exception as e:
            # Handle specific errors for better error messages
            error_msg = str(e)
            if "unexpected EOF" in error_msg or "was never closed" in error_msg:
                open_brackets = expr.count('(')
                close_brackets = expr.count(')')
                if open_brackets > close_brackets:
                    raise ValueError(f"Missing {open_brackets - close_brackets} closing bracket(s)")
                
            # For division by zero, give a specific error
            if "division by zero" in error_msg:
                raise ValueError("Cannot divide by zero")
            
            # Re-raise with the original error
            raise
    
    def calculate(self):
        if not self.expression:
            return
        
        try:
            # Recalculate bracket count to ensure accuracy
            open_count = self.expression.count('(')
            close_count = self.expression.count(')')
            self.bracket_count = open_count - close_count
            
            # Process the expression to handle implicit multiplication
            processed_expr = self.preprocess_expression(self.expression)
            
            # Add closing brackets if needed
            closing_brackets = ""
            for _ in range(self.bracket_count):
                closing_brackets += ")"
            
            # Combine the expression with any needed closing brackets
            full_expression = self.expression + closing_brackets
            processed_expr_full = processed_expr
            
            # Evaluate the expression
            result = self.safe_eval(processed_expr_full)
            
            # Format the result
            if isinstance(result, float):
                # Check if result is close to an integer
                if abs(result - round(result)) < 1e-10:
                    formatted_result = str(int(round(result)))
                else:
                    # Format to show at most 8 decimal places
                    formatted_result = f"{result:.8f}".rstrip("0").rstrip(".")
            else:
                formatted_result = str(result)
            
            # Add to history
            self.add_to_history(full_expression, formatted_result)
            
            # Update display
            self.result_var.set(formatted_result)
            
            # Update the expression to the result
            self.expression = formatted_result
            self.expression_var.set(self.expression)
            
            # Reset bracket count
            self.bracket_count = 0
            self.update_bracket_indicator()
            
            # Update cursor position to end
            self.cursor_position = len(self.expression)
            self.display.icursor(self.cursor_position)
            self.update_cursor_position()
            
        except Exception as e:
            # Handle calculation errors more gracefully
            error_msg = str(e)
            
            # For bracket errors, just show the message in the result area
            if "never closed" in error_msg or "missing" in error_msg.lower() and "bracket" in error_msg.lower():
                self.result_var.set(f"Add {self.bracket_count} bracket(s)")
            elif "division by zero" in error_msg.lower():
                self.result_var.set("Cannot divide by zero")
            else:
                # For other errors, show a dialog
                messagebox.showerror("Error", f"Invalid expression: {error_msg}")
                
                # Only reset expression for non-bracket errors
                self.expression = ""
                self.expression_var.set("")
                self.result_var.set("0")
                self.bracket_count = 0
                self.update_bracket_indicator()
                
                # Reset cursor position
                self.cursor_position = 0
                self.display.icursor(0)
                self.update_cursor_position()
    
    def add_to_history(self, expression, result):
        # Add calculation to history (keep last 3 only)
        history_item = f"{expression} = {result}"
        self.history.insert(0, history_item)
        
        # Keep only the last 3 entries
        if len(self.history) > 3:
            self.history = self.history[:3]
        
        # Update history display
        self.history_var.set("\n".join(self.history))

if __name__ == "__main__":
    # Default to GUI calculator
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop() 