"""
Utils Layer - Async Utilities
Threading helpers for GUI responsiveness
"""
import threading
import traceback
from typing import Callable, Any, Optional, List

class ThreadedTask(threading.Thread):
    """Threaded task executor with callbacks."""
    
    def __init__(self, task_func: Callable, on_success: Callable, on_error: Callable):
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


def run_async(root, func: Callable, on_success_callback: Callable, 
              on_error_callback: Callable, status_label=None, buttons_to_disable: Optional[List] = None):
    """
    Run func() in thread with proper error handling.
    
    Args:
        root: Tkinter root window
        func: Function to run in background
        on_success_callback: Called on success
        on_error_callback: Called on error
        status_label: Optional label to update with status
        buttons_to_disable: Optional list of buttons to disable during execution
    """
    if buttons_to_disable:
        for b in buttons_to_disable:
            b.config(state='disabled')
    if status_label:
        status_label.config(text="Running...")

    def _on_success_thread(result):
        root.after(0, lambda: _on_success_main(result))

    def _on_error_thread(e):
        root.after(0, lambda: _on_error_main(e))

    def _on_success_main(result):
        if status_label:
            status_label.config(text="Done")
        if buttons_to_disable:
            for b in buttons_to_disable:
                b.config(state='normal')
        on_success_callback(result)

    def _on_error_main(e):
        if status_label:
            status_label.config(text="Error")
        if buttons_to_disable:
            for b in buttons_to_disable:
                b.config(state='normal')
        on_error_callback(e)

    task = ThreadedTask(func, _on_success_thread, _on_error_thread)
    task.start()
