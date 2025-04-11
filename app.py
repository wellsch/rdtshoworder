import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import pandas as pd
from collections import defaultdict


class FileUploadApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("RDT Show Order Creator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.file_path = None
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Application title
        self.title_label = tk.Label(
            self.main_frame, 
            text="RDT Show Order Creator", 
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Instructions
        self.instructions = tk.Label(
            self.main_frame,
            text="Upload a dance .xlsx or .xls file",
            font=("Arial", 10)
        )
        self.instructions.pack(pady=10)
        
        # Upload button
        self.upload_button = tk.Button(
            self.main_frame,
            text="Select Excel File",
            command=self.select_file,
            width=20,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.upload_button.pack(pady=10)
        
        # File path display
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("No file selected")
        self.file_path_label = tk.Label(
            self.main_frame,
            textvariable=self.file_path_var,
            font=("Arial", 10),
            wraplength=400
        )
        self.file_path_label.pack(pady=10)
        
        # Process file button (initially disabled)
        self.process_button = tk.Button(
            self.main_frame,
            text="Process File",
            command=self.process_file,
            width=20,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.process_button.pack(pady=10)
        
        # Results area
        self.results_label = tk.Label(
            self.main_frame,
            text="Results:",
            font=("Arial", 10, "bold")
        )
        self.results_label.pack(pady=(10, 5), anchor="w")
        
        self.results_text = scrolledtext.ScrolledText(
            self.main_frame,
            width=80,
            height=15,
            font=("Courier", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg="#666666"
        )
        self.status_label.pack(pady=10)
    
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
            self.results_text.delete(1.0, tk.END)
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
            
            # Display the results
            self.display_results(dance_roster)
            
            # Update status
            self.status_var.set(f"Successfully processed {Path(self.file_path).name}")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")

    def display_results(self, dance_roster):
        """Display the dance roster results in the text area"""
        if not dance_roster:
            self.results_text.insert(tk.END, "No dance data found in the file.")
            return
        
        # Display the dance roster information
        total_dances = len(dance_roster)
        total_dancers = sum(len(dancers) for dancers in dance_roster.values())
        
        self.results_text.insert(tk.END, f"Found {total_dances} dances with {total_dancers} total dancers.\n\n")
        
        # Display each dance and its dancers
        for dance_name, dancers in dance_roster.items():
            self.results_text.insert(tk.END, f"Dance: {dance_name} ({len(dancers)} dancers)\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            
            for i, dancer in enumerate(dancers, 1):
                self.results_text.insert(tk.END, f"{i}. {dancer}\n")
            
            self.results_text.insert(tk.END, "\n")
        
        # Save the dance data for potential further processing
        self.dance_data = dance_roster