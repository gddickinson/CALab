#!/usr/bin/env python3
"""
CALab - Cellular Automata Laboratory
Main GUI Application Launcher

Run with: python main.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui.main_window import CALabMainWindow


def main():
    """Main entry point for GUI application"""
    
    print("\n" + "=" * 60)
    print("CALab - Cellular Automata Laboratory")
    print("=" * 60)
    print("Loading GUI...")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("CALab")
    app.setOrganizationName("CALab")
    
    # Set application style (optional - looks better on some systems)
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CALabMainWindow()
    window.show()
    
    print("✓ GUI ready!")
    print("=" * 60)
    print()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
