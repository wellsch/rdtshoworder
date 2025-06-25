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
        self.root.title("Vertical Dance Roster Manager")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        
        self.file_path = None
        self.dance_data = None
        self.dance_boxes = []
        self.vertical_slots = []  # Y-coordinates of valid positions
        self.slot_height = 100    # Height between slots
        self.margin_top = 80      # Top margin
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top section (file handling)
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=10)
        
        # Application title
        self.title_label = tk.Label(
            self.top_frame, 
            text="Vertical Dance Order Manager", 
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
            text="Reset Order",
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
            wraplength=650
        )
        self.file_path_label.pack(fill=tk.X, pady=5)
        
        # Instructions label
        self.instructions_label = tk.Label(
            self.main_frame,
            text="Drag dances vertically to reorder. Click the lock icon to lock/unlock a dance position.",
            font=("Arial", 10, "italic"),
            fg="#666666"
        )
        self.instructions_label.pack(fill=tk.X, pady=5)
        
        # Canvas for drag and drop interface
        self.canvas_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollbar (only vertical)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=550,
            height=500,
            scrollregion=(0, 0, 550, 1000),
            yscrollcommand=self.v_scrollbar.set,
            bg="white"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
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
            self.vertical_slots = []
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
        """Display dance objects as vertically ordered draggable boxes on the canvas"""
        # Clear any existing content
        self.canvas.delete("all")
        self.dance_boxes: list[DanceBox] = []
        self.vertical_slots = []
        
        # Display summary at the top
        self.canvas.create_text(
            20, 20,
            text=f"Found {len(dances)} dances with {len(dancers)} total dancers",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        
        # Create guide line down the middle
        self.canvas.create_line(
            50, self.margin_top, 50, self.margin_top + len(dances) * self.slot_height,
            fill="#BBDEFB", width=2, dash=(4, 4)
        )
        
        # Create dance boxes in vertical order
        for i, dance in enumerate(dances):
            # Set position property
            dance.position = i
            
            # Calculate vertical position
            y_position = self.margin_top + i * self.slot_height
            self.vertical_slots.append(y_position)
            
            # Create the dance box
            dance_box = DanceBox(self, self.canvas, y_position, dance)
            self.dance_boxes.append(dance_box)
        
        # Update canvas scroll region
        total_height = self.margin_top + len(dances) * self.slot_height + 50
        self.canvas.config(scrollregion=(0, 0, 550, total_height))
        
        # Save the dance data for potential further processing
        self.dance_data = (dances, dancers)
    
    def find_nearest_slot(self, dragged_box):
        """Find the nearest vertical slot to snap to and the corresponding position"""
        # Check if any slots are available
        if not self.vertical_slots:
            return dragged_box.y, dragged_box.dance.position
        
        # Initialize variables
        min_distance = float('inf')
        nearest_slot = dragged_box.y
        box_center_y = dragged_box.y + dragged_box.height / 2
        position = dragged_box.dance.position
        old_position = position
        
        # Create a list of available slots that are not occupied by locked boxes
        locked_slots = set()
        for box in self.dance_boxes:
            if box.dance.locked and box != dragged_box:
                locked_slots.add(box.vertical_slot)
        
        available_slots = [slot for slot in self.vertical_slots if slot not in locked_slots]
        if not available_slots:
            # If all slots are locked, keep original position
            return dragged_box.vertical_slot, dragged_box.dance.position
        
        # Find the nearest available slot
        for i, slot in enumerate(available_slots):
            distance = abs(box_center_y - (slot + dragged_box.height / 2))
            if distance < min_distance:
                min_distance = distance
                nearest_slot = slot
                position = i
        
        return nearest_slot, position, old_position
    
    def update_all_positions(self):
        """Update all position indicators based on vertical order"""
        # Sort dance boxes by vertical position
        sorted_boxes = sorted(self.dance_boxes, key=lambda box: box.y)
        
        # Update position indicators
        for i, box in enumerate(sorted_boxes):
            box.update_position_indicator(i)
    
    def save_order(self):
        """Save the current order of dances based on their vertical position"""
        if not self.dance_boxes:
            messagebox.showinfo("Info", "No dances to save order for.")
            return
        
        # Sort dance boxes by vertical position
        sorted_boxes = sorted(self.dance_boxes, key=lambda box: box.y)
        
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
        """Reset the layout of dance boxes to the original order"""
        if not self.dance_data:
            return
            
        dances, dancers = self.dance_data
        
        # Reset the positions and locked state
        for dance in dances:
            dance.locked = False
        
        # Redisplay with original order
        self.display_results(dances, dancers)
        self.status_var.set("Order reset to original sequence.")