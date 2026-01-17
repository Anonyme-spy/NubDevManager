import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLabel, QPushButton,
                             QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
import os

# Import content pages
from pages.home_page import HomePage
from pages.individual_tools_page import IndividualToolsPage
from pages.dev_packs_page import DevPacksPage
from pages.aur_installer_page import AURInstallerPage
from pages.logs_page import LogsPage
from pages.settings_page import SettingsPage
from core.package_manager import PackageManager


class DevManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dev Manager")
        self.setGeometry(100, 100, 1200, 700)

        # Store reference to navigation buttons for styling
        self.nav_buttons = []

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Create main content area with stacked widget
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area)

        self.load_stylesheets()



    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(190)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo section at the top
        logo_widget = QWidget()
        logo_widget.setObjectName("logoSection")
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(15, 20, 15, 20)

        logo_title = QLabel("Dev Manager")
        logo_title.setObjectName("logoTitle")
        logo_subtitle = QLabel("Linux Dev Tools")
        logo_subtitle.setObjectName("logoSubtitle")

        logo_layout.addWidget(logo_title)
        logo_layout.addWidget(logo_subtitle)
        layout.addWidget(logo_widget)

        # Navigation items - each button will switch to a different page
        nav_items = [
            ("🏠", "Home", 0),
            ("🔧", "Individual Tools", 1),
            ("📦", "Dev Packs", 2),
            ("📥", "AUR Installer", 3),
            ("📋", "Logs", 4),
            ("⚙", "Settings", 5)
        ]

        # Create navigation buttons and connect them to page switching
        for icon, text, page_index in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("navButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            # Connect button click to switch pages
            btn.clicked.connect(lambda checked, idx=page_index, b=btn: self.switch_page(idx, b))

            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        # Set first button as active
        self.nav_buttons[0].setObjectName("navButtonActive")

        layout.addStretch()

        # User section at bottom
        user_widget = QWidget()
        user_widget.setObjectName("userSection")
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(15, 15, 15, 15)

        user_label = QLabel("👤")
        user_label.setObjectName("userIcon")
        user_name = QLabel("DevUser\nuser@linux")
        user_name.setObjectName("userName")

        user_layout.addWidget(user_label)
        user_layout.addWidget(user_name)
        user_layout.addStretch()

        layout.addWidget(user_widget)

        return sidebar

    def create_content_area(self):
        """Create the main content area with stacked widget for different pages"""
        content_frame = QFrame()
        content_frame.setObjectName("content")

        layout = QVBoxLayout(content_frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header that shows current page title
        self.header = self.create_header()
        layout.addWidget(self.header)

        # Stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()

        # Add all pages to the stacked widget
        self.stacked_widget.addWidget(HomePage())  # Index 0
        self.stacked_widget.addWidget(IndividualToolsPage())  # Index 1
        self.stacked_widget.addWidget(DevPacksPage())  # Index 2
        self.stacked_widget.addWidget(AURInstallerPage())  # Index 3
        self.stacked_widget.addWidget(LogsPage())  # Index 4
        self.stacked_widget.addWidget(SettingsPage())  # Index 5

        layout.addWidget(self.stacked_widget)

        return content_frame

    def create_header(self):
        """Create the header bar with page title and status indicators"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Page title (will be updated when switching pages)
        self.header_title = QLabel("Home")
        self.header_title.setObjectName("headerTitle")
        layout.addWidget(self.header_title)

        layout.addStretch()

        # Status indicators on the right
        connected = QLabel("● Connected")
        connected.setObjectName("statusConnected")

        pm = PackageManager()
        distro_info = pm.distro
        distro = QLabel(distro_info.get("name", "Unknown"))
        distro.setObjectName("statusOS")

        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("settingsButton")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(connected)
        layout.addWidget(distro)
        layout.addWidget(settings_btn)

        return header

    def switch_page(self, page_index, clicked_button):
        """Switch to a different page and update header title"""
        # Update the stacked widget to show the selected page
        self.stacked_widget.setCurrentIndex(page_index)

        # Update header title based on page
        page_titles = ["Home", "Individual Tools", "Dev Packs", "AUR Installer", "Logs", "Settings"]
        self.header_title.setText(page_titles[page_index])

        # Update navigation button styles - reset all to inactive, set clicked to active
        for btn in self.nav_buttons:
            btn.setObjectName("navButton")
            btn.setStyle(btn.style())  # Force style refresh

        clicked_button.setObjectName("navButtonActive")
        clicked_button.setStyle(clicked_button.style())  # Force style refresh

    def load_stylesheets(self):
        """Load all stylesheets"""
        styles_dir = os.path.join(os.path.dirname(__file__), 'styles')
        combined_styles = ""

        for qss_file in os.listdir(styles_dir):
            if qss_file.endswith('.qss'):
                with open(os.path.join(styles_dir, qss_file), 'r') as f:
                    combined_styles += f.read() + "\n"

        self.setStyleSheet(combined_styles)
