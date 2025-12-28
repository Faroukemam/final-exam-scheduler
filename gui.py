# gui.py - Layered Architecture
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import traceback

# --- Layered Imports ---
# Presentation Layer
from presentation.styles import COLORS, WINDOW_SIZES
from presentation.gui.widgets import ModernButton, AppBase

# Data Layer
from data.templates import template_generator

# Utils Layer
from utils.async_utils import run_async

# Business Layer
try:
    import exam_optimizer
    import invigilation_optimizer
except ImportError as e:
    pass  # Managed in the functions

# Note: ThreadedTask and run_async now imported from utils.async_utils

# Keeping local legacy placeholder for compatibility (can be removed later)
# class ThreadedTask(threading.Thread):
    def __init__(self, task_func, on_success, on_error):
        super().__init__()
        self.task_func = task_func
        self.on_success = on_success
        self.on_error = on_error
        self.daemon = True

    def run(self):
        try:
            result = self.task_func()
            self.on_success(result)
        except Exception as e:
            self.on_error(e)

def run_async(root, func, on_success_callback, on_error_callback, status_label=None, buttons_to_disable=None):
    """Run func() in thread with proper error handling."""
    if buttons_to_disable:
        for b in buttons_to_disable:
            b.config(state='disabled')
            
    if status_label:
        status_label.config(text="⏳ Running...", foreground=COLORS['accent_secondary'])

    def _on_success_thread(result):
        root.after(0, lambda: _on_success_main(result))

    def _on_error_thread(e):
        root.after(0, lambda err=e: _on_error_main(err))

    def _on_success_main(result):
        if buttons_to_disable:
            for b in buttons_to_disable:
                b.config(state='normal')
        if status_label:
            status_label.config(text="✓ Done", foreground=COLORS['accent_success'])
        try:
            on_success_callback(result)
        except Exception as e:
            _on_error_main(e)

    def _on_error_main(e):
        if buttons_to_disable:
            for b in buttons_to_disable:
                b.config(state='normal')
        if status_label:
            status_label.config(text="✗ Error", foreground=COLORS['accent_error'])
        on_error_callback(e)

    task = ThreadedTask(func, _on_success_thread, _on_error_thread)
    task.start()

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

class AppBase:
    """Modern styled sub-window with template generation support."""
    def __init__(self, master, title, help_text=""):
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry("800x750")
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
                                      f"Templates created successfully!\n\nGenerated {len(files)} file(s):\n" + 
                                      "\n".join(f"✓ {f}" for f in files))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate templates:\n{e}")
        
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

# --- Mini Apps ---

def open_exam_scheduler(root):
    app = AppBase(root, "Final Exam Scheduler")
    
    # Template Generation
    app.add_template_button(template_generator.generate_exam_scheduler_templates)
    
    app.add_file_picker("Regs File:", "regs")
    app.add_file_picker("Courses Master:", "master")
    app.add_file_picker("Calendar:", "cal")
    app.add_file_picker("Slot Capacity:", "cap")
    app.add_file_picker("Constraints:", "cons")
    app.add_save_picker("Output Path:", "out", "Final_Exam_Schedule.xlsx")
    
    # Rest Days
    f = tk.Frame(app.content, bg=COLORS['bg_dark'])
    f.pack(fill='x', pady=8)
    tk.Label(f, text="Rest Days:", width=18, anchor='w',
            font=('Segoe UI', 10), bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']).pack(side='left', padx=(0, 10))
    e_rest = tk.Entry(f, font=('Segoe UI', 10), bg=COLORS['bg_light'],
                     fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'],
                     relief='flat', bd=0, width=10)
    e_rest.insert(0, "1")
    e_rest.pack(side='left', ipady=8)
    
    status_lbl = tk.Label(app.top, text="Ready", font=('Segoe UI', 10),
                         bg=COLORS['bg_dark'], fg=COLORS['text_secondary'])
    status_lbl.pack(pady=15)
    
    def run_logic():
        import exam_optimizer 
        
        regs = app.get_path("regs")
        master = app.get_path("master")
        cal = app.get_path("cal")
        cap = app.get_path("cap")
        cons = app.get_path("cons")
        out = app.get_path("out")
        
        if not (regs and master and cal and cap):
            raise ValueError("Please select all required input files.")
            
        rest = int(e_rest.get())
        
        exam_optimizer.run_final_exam_scheduler(
            regs_path=regs,
            courses_master_path=master,
            calendar_path=cal,
            slot_capacity_path=cap,
            constraints_path=cons,
            output_path=out,
            rest_days=rest,
            diagnostics_only=False
        )
        return out

    def on_ok(res):
        messagebox.showinfo("Success", f"Schedule created:\n{res}")
        
    def on_fail(e):
        messagebox.showerror("Error", f"Failed:\n{e}\n\n{traceback.format_exc()}")

    btn = ModernButton(app.top, "Run Scheduler", 
                      lambda: run_async(app.top, run_logic, on_ok, on_fail, status_lbl, [btn]))
    btn.pack(pady=20)

def open_diagnostics(root):
    app = AppBase(root, "Exam Data Diagnostics")
    
    # Template Generation (uses same templates as exam scheduler)
    app.add_template_button(template_generator.generate_exam_scheduler_templates)
    
    app.add_file_picker("Regs File:", "regs")
    app.add_file_picker("Courses Master:", "master")
    app.add_file_picker("Calendar:", "cal", "")
    app.add_file_picker("Slot Capacity:", "cap", "")
    app.add_save_picker("Output Path:", "out", "Diagnostics.xlsx")
    
    status_lbl = tk.Label(app.top, text="Ready", font=('Segoe UI', 10),
                         bg=COLORS['bg_dark'], fg=COLORS['text_secondary'])
    status_lbl.pack(pady=15)
    
    def run_logic():
        import exam_optimizer
        
        regs = app.get_path("regs")
        master = app.get_path("master")
        cal = app.get_path("cal") or "dummy"
        cap = app.get_path("cap") or "dummy"
        cons = ""
        out = app.get_path("out")
        
        if not (regs and master):
             raise ValueError("Regs and Master are minimum required.")

        diag, dfs = exam_optimizer.run_final_exam_scheduler(
            regs_path=regs,
            courses_master_path=master,
            calendar_path=cal,
            slot_capacity_path=cap,
            constraints_path=cons,
            output_path=out,
            diagnostics_only=True
        )
        
        exam_optimizer.save_diagnostics_excel(dfs, out)
        return out

    def on_ok(res):
        messagebox.showinfo("Success", f"Diagnostics saved:\n{res}")
        
    def on_fail(e):
        messagebox.showerror("Error", f"Failed:\n{e}\n\n{traceback.format_exc()}")

    btn = ModernButton(app.top, "Run Diagnostics",
                      lambda: run_async(app.top, run_logic, on_ok, on_fail, status_lbl, [btn]))
    btn.pack(pady=20)

def open_courses_report(root):
    app = AppBase(root, "Courses Report Builder")
    
    # Template Generation
    app.add_template_button(template_generator.generate_courses_report_templates)
    
    app.add_file_picker("Regs File:", "regs")
    app.add_file_picker("Courses Master:", "master")
    app.add_save_picker("Output Path:", "out", "Courses_Report.xlsx")
    
    status_lbl = tk.Label(app.top, text="Ready", font=('Segoe UI', 10),
                         bg=COLORS['bg_dark'], fg=COLORS['text_secondary'])
    status_lbl.pack(pady=15)
    
    def run_logic():
        import exam_optimizer
        regs = app.get_path("regs")
        master = app.get_path("master")
        out = app.get_path("out")
        
        if not (regs and master):
             raise ValueError("Select inputs.")
             
        report, issues = exam_optimizer.generate_courses_report(regs, master)
        exam_optimizer.save_courses_report_excel(report, issues, out)
        return out

    def on_ok(res):
        messagebox.showinfo("Success", f"Report saved:\n{res}")
        
    def on_fail(e):
        messagebox.showerror("Error", f"Failed:\n{e}\n\n{traceback.format_exc()}")

    btn = ModernButton(app.top, "Build Courses Report",
                      lambda: run_async(app.top, run_logic, on_ok, on_fail, status_lbl, [btn]))
    btn.pack(pady=20)

def open_invigilation(root):
    app = AppBase(root, "Invigilation Scheduler")
    
    # Template Generation
    app.add_template_button(template_generator.generate_invigilation_templates)
    
    app.add_file_picker("Sessions:", "sess")
    app.add_file_picker("Staff:", "staff")
    app.add_file_picker("Engagement:", "engage")
    app.add_save_picker("Output Path:", "out", "Invigilation_Schedule.xlsx")
    
    status_lbl = tk.Label(app.top, text="Ready", font=('Segoe UI', 10),
                         bg=COLORS['bg_dark'], fg=COLORS['text_secondary'])
    status_lbl.pack(pady=15)
    
    def run_logic():
        import invigilation_optimizer
        sess = app.get_path("sess")
        staff = app.get_path("staff")
        engage = app.get_path("engage")
        out = app.get_path("out")
        
        if not (sess and staff):
            raise ValueError("Sessions and Staff files required.")
            
        res = invigilation_optimizer.run_optimization(sess, staff, engage, out)
        return out

    def on_ok(res):
        messagebox.showinfo("Success", f"Schedule created:\n{res}")
        
    def on_fail(e):
        messagebox.showerror("Error", f"Failed:\n{e}\n\n{traceback.format_exc()}")

    btn = ModernButton(app.top, "Run Invigilation",
                      lambda: run_async(app.top, run_logic, on_ok, on_fail, status_lbl, [btn]))
    btn.pack(pady=20)

# --- Main Launcher ---

# --- About Dialog ---

def show_about_dialog(parent):
    """Display About dialog with copyright and contact information."""
    about = tk.Toplevel(parent)
    about.title("About")
    about.geometry("580x520")
    about.configure(bg=COLORS['bg_dark'])
    about.resizable(False, False)
    
    # Header
    header = tk.Frame(about, bg=COLORS['bg_medium'], height=80)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    tk.Label(header, text="📊", font=('Segoe UI', 28),
            bg=COLORS['bg_medium'], fg=COLORS['accent_primary']).pack(pady=5)
    
    tk.Label(header, text="Final Exam Scheduler", 
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_medium'], fg=COLORS['text_primary']).pack()
    
    # Content
    content = tk.Frame(about, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=30, pady=20)
    
    # Version
    tk.Label(content, text="Desktop Application", 
            font=('Segoe UI', 10),
            bg=COLORS['bg_dark'], fg=COLORS['text_secondary']).pack(pady=(0, 5))
    
    tk.Label(content, text="Version 1.1", 
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['accent_primary']).pack(pady=(0, 20))
    
    # Separator
    separator = tk.Frame(content, bg=COLORS['border'], height=1)
    separator.pack(fill='x', pady=15)
    
    # Copyright
    tk.Label(content, text="© 2025 Eng. Farouk Emam Waked", 
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(pady=(0, 5))
    
    tk.Label(content, text="All rights reserved.", 
            font=('Segoe UI', 9),
            bg=COLORS['bg_dark'], fg=COLORS['text_secondary']).pack(pady=(0, 15))
    
    # Legal notice
    legal_text = (
        "This software and its source code are protected by copyright laws.\n\n"
        "Unauthorized copying, modification, distribution, or commercial use\n"
        "is prohibited without explicit written permission from the author."
    )
    
    legal_frame = tk.Frame(content, bg=COLORS['bg_light'], relief='flat', bd=0)
    legal_frame.pack(fill='x', pady=10, padx=10)
    
    tk.Label(legal_frame, text=legal_text, 
            font=('Segoe UI', 8),
            bg=COLORS['bg_light'], fg=COLORS['text_secondary'],
            justify='center').pack(pady=15, padx=15)
    
    # Separator
    separator2 = tk.Frame(content, bg=COLORS['border'], height=1)
    separator2.pack(fill='x', pady=15)
    
    # Contact Information
    tk.Label(content, text="Contact Information", 
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(pady=(0, 10))
    
    contact_info = [
        ("👤 Author:", "Eng. Farouk Emam Waked"),
        ("📧 Email:", "farouk.waked@must.edu.eg"),
        ("📱 Phone/WhatsApp:", "+201092527272"),
    ]
    
    for icon_label, value in contact_info:
        info_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        info_frame.pack(fill='x', pady=3)
        
        tk.Label(info_frame, text=icon_label, 
                font=('Segoe UI', 9),
                bg=COLORS['bg_dark'], fg=COLORS['text_secondary'],
                width=20, anchor='e').pack(side='left', padx=(0, 10))
        
        tk.Label(info_frame, text=value, 
                font=('Segoe UI', 9, 'bold'),
                bg=COLORS['bg_dark'], fg=COLORS['accent_secondary'],
                anchor='w').pack(side='left')
    
    # Close button
    close_btn = ModernButton(about, "Close", about.destroy, width=120, height=40)
    close_btn.pack(pady=20)

# --- Main Launcher ---

def main():
    root = tk.Tk()
    root.title("Final Exam Scheduler v1.1")
    root.geometry("520x620")
    root.configure(bg=COLORS['bg_dark'])
    
    # Header
    header_frame = tk.Frame(root, bg=COLORS['bg_medium'], height=120)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Logo
    logo_loaded = False
    if os.path.exists("assets/logo.png"):
        try:
            img = tk.PhotoImage(file="assets/logo.png")
            # Subsample to smaller size
            img = img.subsample(3, 3)
            lbl = tk.Label(header_frame, image=img, bg=COLORS['bg_medium'])
            lbl.image = img
            lbl.pack(pady=10)
            logo_loaded = True
        except:
            pass
    
    if not logo_loaded:
        tk.Label(header_frame, text="📊", font=('Segoe UI', 32),
                bg=COLORS['bg_medium'], fg=COLORS['accent_primary']).pack(pady=5)
    
    tk.Label(header_frame, text="Final Exam Scheduler", 
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['bg_medium'], fg=COLORS['text_primary']).pack()
    
    # Main content
    content = tk.Frame(root, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=40, pady=30)
    
    tk.Label(content, text="Choose a Tool", font=('Segoe UI', 14),
            bg=COLORS['bg_dark'], fg=COLORS['text_secondary']).pack(pady=(0, 20))
    
    # Tool buttons
    tools = [
        ("📝 Exam Scheduler", open_exam_scheduler),
        ("🔍 Diagnostics & Checks", open_diagnostics),
        ("📊 Courses Report", open_courses_report),
        ("👥 Invigilation Scheduler", open_invigilation),
    ]
    
    for text, cmd in tools:
        btn = ModernButton(content, text, lambda c=cmd: c(root), width=300, height=55)
        btn.pack(pady=8)
    
    # Footer with About button
    footer = tk.Frame(root, bg=COLORS['bg_dark'])
    footer.pack(fill='x', padx=40, pady=(20, 20))
    
    tk.Label(footer, text="v1.1", 
            font=('Segoe UI', 8),
            bg=COLORS['bg_dark'], fg=COLORS['text_secondary']).pack(pady=(0, 8))
    
    about_btn = ModernButton(footer, "About", lambda: show_about_dialog(root), width=120, height=35)
    about_btn.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
