#!/usr/bin/env python3
"""
Dev Manager - Linux Development Tools Manager
Entry point for the application
"""

import sys
import os

# Add UI directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'UI'))

from PyQt6.QtWidgets import QApplication
from UI.app import DevManager


def main():
    """Main entry point for Dev Manager application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Dev Manager")
    app.setApplicationVersion("1.0.0")

    window = DevManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
