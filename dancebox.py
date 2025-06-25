from typing import Tuple

from dance import Dance


class DanceBox:
    def __init__(self, app, canvas, y_position, dance: Dance, width=450, height=80, 
                 x_margin=50, box_color="#E1F5FE", hover_color="#B3E5FC"):
        self.app = app
        self.canvas = canvas
        self.dance = dance
        self.width = width
        self.height = height
        self.x = x_margin
        self.y = y_position
        self.vertical_slot = y_position  # Remember the slot this box belongs to
        self.box_color = box_color
        self.hover_color = hover_color
        self.snap_threshold = 20  # Threshold for snapping
        
        # Create the box
        self.box = canvas.create_rectangle(
            self.x, self.y, self.x + width, self.y + height, 
            fill=box_color, outline="#2196F3", width=2,
            tags=("dance_box", f"box_{id(dance)}")
        )
        
        # Create the title
        self.title = canvas.create_text(
            self.x + 15, self.y + 25, 
            text=dance.name, 
            font=("Arial", 12, "bold"), 
            anchor="w",
            tags=(f"title_{id(dance)}")
        )
        
        # Create dancer count
        self.dancer_count = canvas.create_text(
            self.x + 15, self.y + 50, 
            text=f"Dancers: {[dancer.name for dancer in dance.dancers]}", 
            font=("Arial", 10), 
            anchor="w",
            tags=(f"count_{id(dance)}")
        )
        
        # Create lock button circle
        self.lock_x = self.x + width - 30
        self.lock_y = self.y + height/2
        self.lock_radius = 15
        self.lock_button = canvas.create_oval(
            self.lock_x - self.lock_radius, self.lock_y - self.lock_radius,
            self.lock_x + self.lock_radius, self.lock_y + self.lock_radius,
            fill="#BBDEFB" if not dance.locked else "#FF9800",
            outline="#1565C0",
            tags=(f"lock_{id(dance)}")
        )
        
        # Create lock icon (lock/unlock emoji)
        self.lock_icon = canvas.create_text(
            self.lock_x, self.lock_y,
            text="🔓" if not dance.locked else "🔒",
            font=("Arial", 12),
            tags=(f"lock_icon_{id(dance)}")
        )
        
        # Add position indicator
        self.position_indicator = canvas.create_text(
            self.x - 25, self.y + height/2,
            text=str(dance.position + 1),
            font=("Arial", 14, "bold"),
            fill="#1565C0",
            tags=(f"position_{id(dance)}")
        )
        
        # Add event bindings for dragging
        for item in [self.box, self.title, self.dancer_count]:
            canvas.tag_bind(item, "<ButtonPress-1>", self.on_press)
            canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
            canvas.tag_bind(item, "<ButtonRelease-1>", self.on_release)
            canvas.tag_bind(item, "<Enter>", self.on_enter)
            canvas.tag_bind(item, "<Leave>", self.on_leave)
        
        # Add event binding for lock button
        canvas.tag_bind(self.lock_button, "<ButtonPress-1>", self.toggle_lock)
        canvas.tag_bind(self.lock_icon, "<ButtonPress-1>", self.toggle_lock)
        
        self.drag_data = {"x": 0, "y": 0, "dragging": False, "original_y": self.y}
        self.all_items = [self.box, self.title, self.dancer_count, 
                          self.lock_button, self.lock_icon, self.position_indicator]
    
    def on_press(self, event):
        if self.dance.locked:
            return
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["dragging"] = True
        self.drag_data["original_y"] = self.y
        
        # Bring this dance box to the front
        for item in self.all_items:
            self.canvas.tag_raise(item)
        
        # Change appearance while dragging
        self.canvas.itemconfig(self.box, fill="#B2DFDB", outline="#00796B", width=3)
    
    def on_drag(self, event):
        if not self.drag_data["dragging"] or self.dance.locked:
            return
        
        # Calculate distance moved - only care about vertical movement
        dy = event.y - self.drag_data["y"]
        
        # Move all elements of the dance box vertically only
        for item in self.all_items:
            self.canvas.move(item, 0, dy)
        
        # Update positions
        self.lock_y += dy
        self.y += dy
        
        # Update drag data
        self.drag_data["y"] = event.y
    
    def on_release(self, event):
        if not self.drag_data["dragging"] or self.dance.locked:
            return
            
        self.drag_data["dragging"] = False
        
        # Reset appearance
        self.canvas.itemconfig(self.box, fill=self.box_color, outline="#2196F3", width=2)
        
        # Find nearest slot and snap to it
        nearest_slot, position, old_position = self.app.find_nearest_slot(self)

        print(nearest_slot, position, old_position)
        
        # Move to the nearest slot
        dy = nearest_slot - self.y
        for item in self.all_items:
            self.canvas.move(item, 0, dy)
        
        # Update positions
        self.lock_y += dy
        self.y = nearest_slot
        self.vertical_slot = nearest_slot
        self.dance.position = position
        
        # Update position indicator
        self.canvas.itemconfig(self.position_indicator, text=str(position + 1))
        
        # Update all position indicators
        self.app.update_all_positions()
    
    def on_enter(self, event):
        if not self.dance.locked:
            self.canvas.itemconfig(self.box, fill=self.hover_color)
    
    def on_leave(self, event):
        if not self.dance.locked and not self.drag_data["dragging"]:
            self.canvas.itemconfig(self.box, fill=self.box_color)
    
    def toggle_lock(self, event):
        self.dance.locked = not self.dance.locked
        
        if self.dance.locked:
            self.canvas.itemconfig(self.lock_button, fill="#FF9800")
            self.canvas.itemconfig(self.lock_icon, text="🔒")
        else:
            self.canvas.itemconfig(self.lock_button, fill="#BBDEFB")
            self.canvas.itemconfig(self.lock_icon, text="🔓")
    
    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def update_position_indicator(self, position):
        """Update the position indicator with the new position"""
        self.dance.position = position
        self.canvas.itemconfig(self.position_indicator, text=str(position + 1))