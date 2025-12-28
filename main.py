"""
Main Application Entry Point
Layered Architecture - Entry point that delegates to presentation layer
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from presentation layer (gui.py acts as presentation layer currently)
import gui

def main():
    """Application entry point."""
    print("=" * 60)
    print("Final Exam Scheduler v1.1")
    print("Layered Architecture")
    print("=" * 60)
    print()
    print("Architecture Layers:")
    print("  - Presentation: GUI components (gui.py)")
    print("  - Business: Optimization logic (exam_optimizer.py, invigilation_optimizer.py)")
    print("  - Data: File I/O and templates (template_generator.py)")
    print("  - Utils: Helper functions (utils/)")
    print()
    print("Starting application...")
    print("=" * 60)
    print()
    
    # Start the GUI (Presentation Layer)
    gui.main()

if __name__ == "__main__":
    main()
