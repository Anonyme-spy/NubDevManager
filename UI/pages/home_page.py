# UI/pages/home_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QScrollArea, QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import subprocess
import shutil
import os
import platform


class HomePage(QWidget):
    """Home page - Dashboard with modern fluid layout"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the home page UI"""
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(24)

        # Hero section with logo
        self.main_layout.addWidget(self.create_hero_section())

        # Stats cards row
        self.main_layout.addWidget(self.create_stats_row())

        # Quick actions
        self.main_layout.addWidget(self.create_quick_actions())

        # System info cards
        self.main_layout.addWidget(self.create_system_info_section())

        # Tip banner
        self.main_layout.addWidget(self.create_info_banner())

        self.main_layout.addStretch()
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

    def create_hero_section(self):
        """Create hero section with logo and welcome message"""
        hero = QFrame()
        hero.setObjectName("heroBanner")
        hero.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout = QHBoxLayout(hero)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(32)

        # Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        logo_label.setObjectName("heroLogo")
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'..', 'assets', 'Linux.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("🐧")
            logo_label.setStyleSheet("font-size: 64px;")

        logo_layout.addWidget(logo_label)
        layout.addWidget(logo_container)

        # Welcome text
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(12)

        username = os.environ.get('USER', 'Developer')
        welcome_label = QLabel(f"Welcome back, {username}!")
        welcome_label.setObjectName("heroTitle")

        subtitle_label = QLabel("Dev Manager — Your productivity hub for Linux development")
        subtitle_label.setObjectName("heroSubtitle")
        subtitle_label.setWordWrap(True)

        desc_label = QLabel("Manage packages, AUR installs, logs and configuration from one sleek interface.")
        desc_label.setObjectName("heroDescription")
        desc_label.setWordWrap(True)

        text_layout.addWidget(welcome_label)
        text_layout.addWidget(subtitle_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch()

        layout.addWidget(text_widget, 1)

        # Action buttons
        btn_widget = QWidget()
        btn_layout = QVBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(12)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_btn = QPushButton("Get Started")
        start_btn.setObjectName("primaryButton")
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.clicked.connect(self.on_update_system)

        docs_btn = QPushButton("Documentation")
        docs_btn.setObjectName("secondaryButton")
        docs_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(docs_btn)

        layout.addWidget(btn_widget)

        return hero

    def create_stats_row(self):
        """Create stats cards row"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        stats = [
            ("📦", "Installed Packages", self.get_installed_packages_count(), "#3B82F6"),
            ("🔄", "Available Updates", self.get_available_updates_count(), "#F59E0B"),
            ("⭐", "AUR Packages", self.get_aur_packages_count(), "#8B5CF6"),
        ]

        for icon, title, value, color in stats:
            card = self.create_stat_card(icon, title, value, color)
            layout.addWidget(card)

        return container

    def create_stat_card(self, icon, title, value, color):
        """Create a single stat card"""
        card = QFrame()
        card.setObjectName("statCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setMinimumHeight(110)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        # Header with icon
        header = QHBoxLayout()
        header.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        header.addWidget(icon_label)
        header.addWidget(title_label)
        header.addStretch()

        # Value
        value_label = QLabel(str(value))
        value_label.setObjectName("statValue")
        value_label.setStyleSheet(f"color: {color};")

        layout.addLayout(header)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def create_quick_actions(self):
        """Create quick action buttons section"""
        section = QFrame()
        section.setObjectName("quickActionsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title = QLabel("Quick Actions")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        buttons = [
            ("🔄  Update System", "primaryButton", self.on_update_system),
            ("🧹  Clean Cache", "secondaryButton", self.on_clean_cache),
            ("🔍  Check Updates", "secondaryButton", self.on_check_updates),
        ]

        for text, obj_name, callback in buttons:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(callback)
            btn_layout.addWidget(btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        return section

    def create_system_info_section(self):
        """Create system information section"""
        section = QFrame()
        section.setObjectName("systemInfoSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title = QLabel("System Information")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        info_layout = QHBoxLayout()
        info_layout.setSpacing(16)

        info_items = [
            ("Operating System", self.get_os_info()),
            ("Package Manager", self.detect_package_manager()),
            ("Kernel Version", platform.release()),
            ("Architecture", platform.machine()),
        ]

        for label, value in info_items:
            item = self.create_info_item(label, value)
            info_layout.addWidget(item)

        layout.addLayout(info_layout)

        return section

    def create_info_item(self, label, value):
        """Create a system info item"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label_widget = QLabel(label)
        label_widget.setObjectName("infoLabel")

        value_widget = QLabel(str(value))
        value_widget.setObjectName("infoValue")
        value_widget.setWordWrap(True)

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        return widget

    def create_info_banner(self):
        """Create info banner"""
        banner = QFrame()
        banner.setObjectName("infoBanner")

        layout = QHBoxLayout(banner)
        layout.setContentsMargins(16, 12, 16, 12)

        label = QLabel("💡 Tip: Use the sidebar navigation to access tools, packages, and system logs.")
        label.setObjectName("infoBannerText")
        label.setWordWrap(True)

        layout.addWidget(label)

        return banner

    def get_os_info(self):
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=")[1].strip().strip('"')
        except:
            pass
        return platform.system()

    def detect_package_manager(self):
        managers = [("pacman", "Pacman"), ("apt", "APT"), ("dnf", "DNF"),
                    ("yum", "YUM"), ("zypper", "Zypper"), ("emerge", "Portage")]
        for cmd, name in managers:
            if shutil.which(cmd):
                return name
        return "Unknown"

    def get_installed_packages_count(self):
        try:
            if shutil.which("pacman"):
                result = subprocess.run(["pacman", "-Q"], capture_output=True, text=True)
                return len([l for l in result.stdout.strip().split('\n') if l])
            elif shutil.which("dpkg"):
                result = subprocess.run(["dpkg", "-l"], capture_output=True, text=True)
                return len([l for l in result.stdout.split('\n') if l.startswith('ii')])
            elif shutil.which("rpm"):
                result = subprocess.run(["rpm", "-qa"], capture_output=True, text=True)
                return len([l for l in result.stdout.strip().split('\n') if l])
        except:
            pass
        return 0

    def get_available_updates_count(self):
        try:
            if shutil.which("pacman"):
                result = subprocess.run(["pacman", "-Qu"], capture_output=True, text=True)
                return len([l for l in result.stdout.strip().split('\n') if l]) if result.stdout.strip() else 0
            elif shutil.which("apt"):
                result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
                return len([l for l in result.stdout.split('\n') if '/' in l])
        except:
            pass
        return 0

    def get_aur_packages_count(self):
        try:
            if shutil.which("pacman"):
                result = subprocess.run(["pacman", "-Qm"], capture_output=True, text=True)
                return len([l for l in result.stdout.strip().split('\n') if l]) if result.stdout.strip() else 0
        except:
            pass
        return 0

    def on_update_system(self):
        pass

    def on_clean_cache(self):
        pass

    def on_check_updates(self):
        pass