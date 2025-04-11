from typing import Tuple

from dance import Dance


class DanceBox:
    def __init__(self, canvas, x, y, dance: Dance, width=250, height=100, box_color="#E1F5FE", hover_color="#B3E5FC"):
        self.canvas = canvas
        self.dance = dance
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.box_color = box_color
        self.hover_color = hover_color
        
        # Create the box
        self.box = canvas.create_rectangle(
            x, y, x + width, y + height, 
            fill=box_color, outline="#2196F3", width=2,
            tags=("dance_box", f"box_{id(dance)}")
        )
        
        # Create the title
        self.title = canvas.create_text(
            x + 10, y + 15, 
            text=dance.name, 
            font=("Arial", 12, "bold"), 
            anchor="w",
            tags=(f"title_{id(dance)}")
        )
        
        # Create dancer count
        self.dancer_count = canvas.create_text(
            x + 10, y + 40, 
            text=f"Dancers: {len(dance.dancers)}", 
            font=("Arial", 10), 
            anchor="w",
            tags=(f"count_{id(dance)}")
        )
        
        # Create lock button circle
        self.lock_x = x + width - 25
        self.lock_y = y + 25
        self.lock_radius = 15
        self.lock_button = canvas.create_oval(
            self.lock_x - self.lock_radius, self.lock_y - self.lock_radius,
            self.lock_x + self.lock_radius, self.lock_y + self.lock_radius,
            fill="#BBDEFB" if not dance.locked else "#FF9800",
            outline="#1565C0",
            tags=(f"lock_{id(dance)}")
        )
        
        # Create lock icon (just an "L" for now)
        self.lock_icon = canvas.create_text(
            self.lock_x, self.lock_y,
            text="🔓" if not dance.locked else "🔒",
            font=("Arial", 12),
            tags=(f"lock_icon_{id(dance)}")
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
        
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
    
    def on_press(self, event):
        if self.dance.locked:
            return
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["dragging"] = True
        
        # Bring this dance box to the front
        self.canvas.tag_raise(self.box)
        self.canvas.tag_raise(self.title)
        self.canvas.tag_raise(self.dancer_count)
        self.canvas.tag_raise(self.lock_button)
        self.canvas.tag_raise(self.lock_icon)
    
    def on_drag(self, event):
        if not self.drag_data["dragging"] or self.dance.locked:
            return
        
        # Calculate distance moved
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        # Move all elements of the dance box
        for item in [self.box, self.title, self.dancer_count, self.lock_button, self.lock_icon]:
            self.canvas.move(item, dx, dy)
        
        # Update lock button coordinates
        self.lock_x += dx
        self.lock_y += dy
        
        # Update drag data
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # Update box position
        self.x += dx
        self.y += dy
    
    def on_release(self, event):
        self.drag_data["dragging"] = False
    
    def on_enter(self, event):
        if not self.dance.locked:
            self.canvas.itemconfig(self.box, fill=self.hover_color)
    
    def on_leave(self, event):
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