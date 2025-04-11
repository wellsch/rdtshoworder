import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import Dict, Set
import pandas as pd
from collections import defaultdict

from dance import Dance
from dancebox import DanceBox
from dancer import Dancer
from dances import process_dances


class DanceRosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag & Drop Dance Roster Manager")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.file_path = None
        self.dance_data = None
        self.dance_boxes = []
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top section (file handling)
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=10)
        
        # Application title
        self.title_label = tk.Label(
            self.top_frame, 
            text="Dance Roster Manager", 
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(side=tk.LEFT, pady=10)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        # Upload button
        self.upload_button = tk.Button(
            self.buttons_frame,
            text="Select Excel File",
            command=self.select_file,
            width=15,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        # Process file button
        self.process_button = tk.Button(
            self.buttons_frame,
            text="Process File",
            command=self.process_file,
            width=15,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        # Save order button
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save Order",
            command=self.save_order,
            width=15,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(
            self.buttons_frame,
            text="Reset Layout",
            command=self.reset_layout,
            width=15,
            bg="#E91E63",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # File path display
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("No file selected")
        self.file_path_label = tk.Label(
            self.main_frame,
            textvariable=self.file_path_var,
            font=("Arial", 10),
            wraplength=800
        )
        self.file_path_label.pack(fill=tk.X, pady=5)
        
        # Canvas for drag and drop interface
        self.canvas_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollbars
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=800,
            height=500,
            scrollregion=(0, 0, 1500, 1000),
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
            bg="white"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg="#666666"
        )
        self.status_label.pack(fill=tk.X, pady=10)
    
    def select_file(self):
        """Open a file dialog to select a file"""
        filetypes = (
            ("Excel files (.xlsx)", "*.xlsx"),
            ("Excel files (.xls)", "*.xls")
        )
        
        selected_file = filedialog.askopenfilename(
            title="Select a file",
            filetypes=filetypes
        )
        
        if selected_file:
            self.file_path = selected_file
            self.file_path_var.set(f"Selected: {selected_file}")
            self.process_button.config(state=tk.NORMAL)
            self.status_var.set("Dance list selected. Click 'Process File' to continue.")
        else:
            self.status_var.set("Dance list selection cancelled.")
    
    def process_file(self):
        """Process the selected Excel file to extract dance rosters"""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        
        try:
            # Clear previous results
            self.canvas.delete("all")
            self.dance_boxes = []
            self.status_var.set("Processing...")
            self.root.update()
            
            # Load the Excel file
            df = pd.read_excel(self.file_path)
            
            # Initialize a dictionary to store dance names and dancers
            dance_roster = defaultdict(list)
            
            # Process each column
            for column in df.columns:
                # Skip unnamed columns
                if 'Unnamed' in str(column):
                    continue
                
                # Get the dance name from the column header
                dance_name = str(column).strip()
                
                if not dance_name:
                    continue
                
                # Get the dancer names from non-empty cells in this column
                dancers = [str(name).strip() for name in df[column].dropna() if str(name).strip()]
                
                # Store dance and dancers in the dictionary
                if dancers:
                    dance_roster[dance_name] = dancers

            dances, all_dancers = process_dances(dance_roster)
            
            # Display the results
            self.display_results(dances, all_dancers)
            
            # Update status
            self.save_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.status_var.set(f"Successfully processed {Path(self.file_path).name}")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")

    def display_results(self, dances: Set["Dance"], dancers: Dict[str, "Dancer"]):
        """Display dance objects as draggable boxes on the canvas"""
        # Clear any existing content
        self.canvas.delete("all")
        self.dance_boxes = []
        
        # Display summary at the top
        self.canvas.create_text(
            20, 20,
            text=f"Found {len(dances)} dances with {len(dancers)} total dancers. Drag boxes to reorder. Click lock icon to lock/unlock.",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        
        # Create dance boxes with initial position
        x, y = 20, 50
        max_x = 0
        row_height = 0
        
        for i, dance in enumerate(dances):
            # Create a new row every 3 dance boxes
            if i > 0 and i % 3 == 0:
                x = 20
                y += row_height + 20
                row_height = 0
            
            # Create the dance box
            dance_box = DanceBox(self.canvas, x, y, dance)
            self.dance_boxes.append(dance_box)
            
            # Update position for next box
            box_width = dance_box.width
            box_height = dance_box.height
            x += box_width + 20
            max_x = max(max_x, x)
            row_height = max(row_height, box_height)
        
        # Update canvas scroll region
        self.canvas.config(scrollregion=(0, 0, max_x, y + row_height + 50))
        
        # Save the dance data for potential further processing
        self.dance_data = (dances, dancers)
    
    def save_order(self):
        """Save the current order of dances based on their vertical position"""
        if not self.dance_boxes:
            messagebox.showinfo("Info", "No dances to save order for.")
            return
        
        # Sort dance boxes by vertical position
        sorted_boxes = sorted(self.dance_boxes, key=lambda box: box.get_position()[1])
        
        # Create a formatted order report
        order_report = "Dance Order:\n\n"
        for i, box in enumerate(sorted_boxes, 1):
            lock_status = "🔒 (Locked)" if box.dance.locked else "🔓 (Unlocked)"
            order_report += f"{i}. {box.dance.name} - {len(box.dance.dancers)} dancers {lock_status}\n"
        
        # Show the order in a dialog
        order_window = tk.Toplevel(self.root)
        order_window.title("Dance Order")
        order_window.geometry("500x400")
        
        # Add a text widget to display the order
        order_text = scrolledtext.ScrolledText(order_window, width=60, height=20)
        order_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        order_text.insert(tk.END, order_report)
        order_text.config(state=tk.DISABLED)
        
        self.status_var.set("Dance order saved.")
    
    def reset_layout(self):
        """Reset the layout of dance boxes to the original grid"""
        if not self.dance_data:
            return
            
        dances, dancers = self.dance_data
        self.display_results(dances, dancers)
        self.status_var.set("Layout reset to default grid.")