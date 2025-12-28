"""
Presentation Layer - Modern Button Widget
Custom button with rounded corners and hover effects
"""
import tkinter as tk
from presentation.styles import COLORS


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects."""
    
    def __init__(self, parent, text, command, **kwargs):
        width = kwargs.pop('width', 280)
        height = kwargs.pop('height', 50)
        
        super().__init__(parent, width=width, height=height, 
                        bg=COLORS['bg_dark'], highlightthickness=0, **kwargs)
        
        self.command = command
        self.text = text
        self.is_hovered = False
        self.is_disabled = False
        
        # Create rounded rectangle
        self.bg_rect = self.create_rounded_rect(2, 2, width-2, height-2, 
                                                radius=12, fill=COLORS['accent_primary'])
        self.text_id = self.create_text(width//2, height//2, text=text, 
                                       fill=COLORS['text_primary'], 
                                       font=('Segoe UI', 11, 'bold'))
        
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1, x2, y1+radius,
                 x2, y2-radius,
                 x2, y2, x2-radius, y2,
                 x1+radius, y2,
                 x1, y2, x1, y2-radius,
                 x1, y1+radius,
                 x1, y1, x1+radius, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def _on_enter(self, e):
        if not self.is_disabled:
            self.is_hovered = True
            self.itemconfig(self.bg_rect, fill=COLORS['accent_secondary'])
            
    def _on_leave(self, e):
        if not self.is_disabled:
            self.is_hovered = False
            self.itemconfig(self.bg_rect, fill=COLORS['accent_primary'])
            
    def _on_click(self, e):
        if not self.is_disabled and self.command:
            self.command()
            
    def config(self, **kwargs):
        if 'state' in kwargs:
            self.is_disabled = (kwargs['state'] == 'disabled')
            if self.is_disabled:
                self.itemconfig(self.bg_rect, fill=COLORS['bg_light'])
                self.itemconfig(self.text_id, fill=COLORS['text_secondary'])
            else:
                self.itemconfig(self.bg_rect, fill=COLORS['accent_primary'])
                self.itemconfig(self.text_id, fill=COLORS['text_primary'])
