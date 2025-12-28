"""
Presentation Layer - Base Window Widget
Reusable base window for tool dialogs with template generation support
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from presentation.styles import COLORS, WINDOW_SIZES


class AppBase:
    """Modern styled sub-window with template generation support."""
    
    def __init__(self, master, title, help_text=""):
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry(WINDOW_SIZES['tool'])
        self.top.configure(bg=COLORS['bg_dark'])
        self.entries = {}
        
        # Header
        header = tk.Frame(self.top, bg=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)
        
        tk.Label(header, text=title, font=('Segoe UI', 18, 'bold'),
                bg=COLORS['bg_medium'], fg=COLORS['text_primary']).pack(pady=15)
        
        # Help text if provided
        if help_text:
            tk.Label(header, text=help_text, font=('Segoe UI', 9),
                    bg=COLORS['bg_medium'], fg=COLORS['text_secondary'],
                    wraplength=700).pack(pady=(0, 10))
        
        # Content frame
        self.content = tk.Frame(self.top, bg=COLORS['bg_dark'])
        self.content.pack(fill='both', expand=True, padx=25)
    
    def add_section_header(self, text):
        """Add a section header for better organization."""
        header_frame = tk.Frame(self.content, bg=COLORS['bg_dark'])
        header_frame.pack(fill='x', pady=(15, 5))
        
        tk.Label(header_frame, text=text, font=('Segoe UI', 11, 'bold'),
                bg=COLORS['bg_dark'], fg=COLORS['accent_secondary']).pack(anchor='w')
        
        # Separator line
        sep = tk.Frame(header_frame, bg=COLORS['border'], height=1)
        sep.pack(fill='x', pady=(5, 0))
    
    def add_file_picker(self, label, key, default="", tooltip=""):
        f = tk.Frame(self.content, bg=COLORS['bg_dark'])
        f.pack(fill='x', pady=6)
        
        label_widget = tk.Label(f, text=label, width=20, anchor='w',
                font=('Segoe UI', 10), bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary'])
        label_widget.pack(side='left', padx=(0, 10))
        
        # Add tooltip if provided
        if tooltip:
            self._create_tooltip(label_widget, tooltip)
        
        e = tk.Entry(f, font=('Segoe UI', 10), bg=COLORS['bg_light'],
                    fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'],
                    relief='flat', bd=0)
        e.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        if default: e.insert(0, default)
        
        def pick():
            path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if path:
                e.delete(0, 'end')
                e.insert(0, path)
        
        btn = tk.Button(f, text="📁 Browse", command=pick,
                       bg=COLORS['accent_primary'], fg=COLORS['text_primary'],
                       font=('Segoe UI', 9), relief='flat', cursor='hand2',
                       padx=15, pady=6)
        btn.pack(side='right')
        self.entries[key] = e
        
    def add_save_picker(self, label, key, default="output.xlsx", tooltip=""):
        f = tk.Frame(self.content, bg=COLORS['bg_dark'])
        f.pack(fill='x', pady=6)
        
        label_widget = tk.Label(f, text=label, width=20, anchor='w',
                font=('Segoe UI', 10), bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary'])
        label_widget.pack(side='left', padx=(0, 10))
        
        if tooltip:
            self._create_tooltip(label_widget, tooltip)
        
        e = tk.Entry(f, font=('Segoe UI', 10), bg=COLORS['bg_light'],
                    fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'],
                    relief='flat', bd=0)
        e.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        e.insert(0, default)
        
        def pick():
            path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if path:
                e.delete(0, 'end')
                e.insert(0, path)
                
        btn = tk.Button(f, text="💾 Save As", command=pick,
                       bg=COLORS['accent_primary'], fg=COLORS['text_primary'],
                       font=('Segoe UI', 9), relief='flat', cursor='hand2',
                       padx=15, pady=6)
        btn.pack(side='right')
        self.entries[key] = e
    
    def add_template_button(self, generator_func, output_dir="."):
        """Add a 'Generate Templates' button."""
        template_frame = tk.Frame(self.content, bg=COLORS['bg_light'], relief='flat')
        template_frame.pack(fill='x', pady=15, ipady=10, ipadx=10)
        
        tk.Label(template_frame, text="🎯 Need help getting started?", 
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_light'], fg=COLORS['text_primary']).pack(pady=(5, 2))
        
        tk.Label(template_frame, 
                text="Generate template files with sample data to understand the expected format.", 
                font=('Segoe UI', 8),
                bg=COLORS['bg_light'], fg=COLORS['text_secondary'],
                wraplength=650).pack(pady=(0, 8))
        
        def generate():
            try:
                folder = filedialog.askdirectory(title="Select folder to save templates")
                if folder:
                    files = generator_func(folder)
                    messagebox.showinfo("Success", 
                                      f"Templates created successfully!\\n\\nGenerated {len(files)} file(s):\\n" + 
                                      "\\n".join(f"✓ {f}" for f in files))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate templates:\\n{e}")
        
        btn = tk.Button(template_frame, text="📄 Generate Template Files", command=generate,
                       bg=COLORS['accent_success'], fg=COLORS['text_primary'],
                       font=('Segoe UI', 10, 'bold'), relief='flat', cursor='hand2',
                       padx=20, pady=8)
        btn.pack()

    def _create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background=COLORS['bg_medium'],
                           foreground=COLORS['text_primary'], relief='solid',
                           borderwidth=1, font=('Segoe UI', 8), padx=8, pady=4)
            label.pack()
            
            widget.tooltip = tooltip
            
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def get_path(self, key):
        return self.entries[key].get().strip()
