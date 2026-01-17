from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QLineEdit, QScrollArea,
                             QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.package_manager import PackageManager


class InstallWorker(QThread):
    """Worker thread for installing/removing packages"""
    finished = pyqtSignal(bool, str)

    def __init__(self, package_manager, package_name, action="install"):
        super().__init__()
        self.pm = package_manager
        self.package_name = package_name
        self.action = action

    def run(self):
        try:
            if self.action == "install":
                success = self.pm.install(self.package_name)
                msg = f"Installed {self.package_name}" if success else f"Failed to install {self.package_name}"
            elif self.action == "remove":
                success = self.pm.remove(self.package_name)
                msg = f"Removed {self.package_name}" if success else f"Failed to remove {self.package_name}"
            else:
                success = False
                msg = "Unknown action"
            self.finished.emit(success, msg)
        except Exception as e:
            self.finished.emit(False, str(e))


class IndividualToolsPage(QWidget):
    """Individual Tools page - Browse and install development tools one by one"""

    def __init__(self):
        super().__init__()
        self.pm = PackageManager()
        self.tool_buttons = {}
        self.workers = []
        self.current_filter = "All"
        self.search_text = ""
        self.init_ui()

    def get_tools_data(self):
        tools = [
            ("Python 3", "High-level programming language", "🐍", "python3", "Languages"),
            ("Node.js", "JavaScript runtime environment", "📗", "nodejs", "Languages"),
            ("Git", "Distributed version control system", "📝", "git", "Version Control"),
            ("Docker", "Container platform", "🐳", "docker", "DevOps"),
            ("PostgreSQL", "Relational database system", "🐘", "postgresql", "Databases"),
            ("VS Code", "Code editor", "📝", "code", "Web Dev"),
            ("Nginx", "Web server", "🌐", "nginx", "Web Dev"),
            ("Redis", "In-memory data store", "🔴", "redis", "Databases"),
            ("MongoDB", "NoSQL database", "🍃", "mongodb", "Databases"),
            ("Go", "Go programming language", "🔵", "go", "Languages"),
            ("Rust", "Rust programming language", "🦀", "rust", "Languages"),
            ("Java", "Java Development Kit", "☕", "default-jdk", "Languages"),
            ("Vim", "Text editor", "📝", "vim", "Web Dev"),
            ("Curl", "Command-line HTTP client", "🌐", "curl", "DevOps"),
            ("Wget", "Network downloader", "📥", "wget", "DevOps"),
            ("htop", "Interactive process viewer", "📊", "htop", "DevOps"),
            ("tmux", "Terminal multiplexer", "🖥", "tmux", "DevOps"),
            ("MySQL", "MySQL database server", "🐬", "mysql-server", "Databases"),
        ]
        return tools

    def init_ui(self):
        """Initialize the individual tools page UI"""
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        # Main scroll area wrapping everything
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        # Page title and description
        title = QLabel("Individual Tools")
        title.setObjectName("pageTitle")
        self.main_layout.addWidget(title)

        desc = QLabel("Browse and install development tools individually")
        desc.setObjectName("pageDescription")
        self.main_layout.addWidget(desc)

        # Search bar
        self.main_layout.addWidget(self.create_search_bar())

        # Category filters
        self.main_layout.addWidget(self.create_filters())

        # Tools grid container
        self.tools_container = QWidget()
        self.tools_layout = QVBoxLayout(self.tools_container)
        self.tools_layout.setContentsMargins(0, 0, 0, 0)
        self.build_tools_grid()
        self.main_layout.addWidget(self.tools_container)

        self.main_layout.addStretch()
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

    def create_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("🔍 Search tools...")
        self.search_input.setFixedHeight(45)
        self.search_input.textChanged.connect(self.on_search_changed)

        search_layout.addWidget(self.search_input)
        return search_container

    def on_search_changed(self, text):
        self.search_text = text.lower()
        self.refresh_tools_grid()

    def create_filters(self):
        filter_container = QWidget()
        self.filter_layout = QHBoxLayout(filter_container)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_layout.setSpacing(10)

        categories = ["All", "Languages", "Version Control", "Databases", "Web Dev", "DevOps"]
        self.filter_buttons = {}

        for i, category in enumerate(categories):
            btn = QPushButton(category)
            btn.setObjectName("filterButtonActive" if i == 0 else "filterButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, cat=category: self.on_filter_clicked(cat))
            self.filter_buttons[category] = btn
            self.filter_layout.addWidget(btn)

        self.filter_layout.addStretch()
        return filter_container

    def on_filter_clicked(self, category):
        self.current_filter = category
        for cat, btn in self.filter_buttons.items():
            btn.setObjectName("filterButtonActive" if cat == category else "filterButton")
            btn.setStyle(btn.style())
        self.refresh_tools_grid()

    def refresh_tools_grid(self):
        # Clear existing grid
        while self.tools_layout.count():
            item = self.tools_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.build_tools_grid()

    def build_tools_grid(self):
        """Build the tools grid widget"""
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)

        tools_data = self.get_tools_data()
        filtered_tools = []

        for tool in tools_data:
            display_name, description, icon, package_name, category = tool
            if self.current_filter != "All" and category != self.current_filter:
                continue
            if self.search_text and self.search_text not in display_name.lower() and self.search_text not in description.lower():
                continue
            filtered_tools.append(tool)

        row, col = 0, 0
        for display_name, description, icon, package_name, category in filtered_tools:
            installed = self.pm.is_installed(package_name)
            tool_card = self.create_tool_card(display_name, description, icon, package_name, installed)
            grid.addWidget(tool_card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.tools_layout.addWidget(grid_widget)

    def create_tool_card(self, name, description, icon, package_name, installed):
        card = QFrame()
        card.setObjectName("toolCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        name_label = QLabel(name)
        name_label.setObjectName("toolName")
        header.addWidget(icon_label)
        header.addWidget(name_label)
        header.addStretch()
        layout.addLayout(header)

        desc_label = QLabel(description)
        desc_label.setObjectName("toolDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        if installed:
            btn = QPushButton("✓ Installed")
            btn.setObjectName("installedButton")
            btn.clicked.connect(lambda: self.on_remove_clicked(package_name, btn))
        else:
            btn = QPushButton("Install")
            btn.setObjectName("installButton")
            btn.clicked.connect(lambda: self.on_install_clicked(package_name, btn))

        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tool_buttons[package_name] = btn
        layout.addWidget(btn)

        return card

    def on_install_clicked(self, package_name, button):
        button.setText("Installing...")
        button.setEnabled(False)
        worker = InstallWorker(self.pm, package_name, "install")
        worker.finished.connect(lambda success, msg: self.on_install_finished(success, msg, package_name, button))
        self.workers.append(worker)
        worker.start()

    def on_remove_clicked(self, package_name, button):
        reply = QMessageBox.question(self, "Confirm Removal", f"Are you sure you want to remove {package_name}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            button.setText("Removing...")
            button.setEnabled(False)
            worker = InstallWorker(self.pm, package_name, "remove")
            worker.finished.connect(lambda success, msg: self.on_remove_finished(success, msg, package_name, button))
            self.workers.append(worker)
            worker.start()

    def on_install_finished(self, success, message, package_name, button):
        button.setEnabled(True)
        if success:
            button.setText("✓ Installed")
            button.setObjectName("installedButton")
            button.setStyle(button.style())
            button.clicked.disconnect()
            button.clicked.connect(lambda: self.on_remove_clicked(package_name, button))
            QMessageBox.information(self, "Success", message)
        else:
            button.setText("Install")
            QMessageBox.warning(self, "Error", message)

    def on_remove_finished(self, success, message, package_name, button):
        button.setEnabled(True)
        if success:
            button.setText("Install")
            button.setObjectName("installButton")
            button.setStyle(button.style())
            button.clicked.disconnect()
            button.clicked.connect(lambda: self.on_install_clicked(package_name, button))
            QMessageBox.information(self, "Success", message)
        else:
            button.setText("✓ Installed")
            QMessageBox.warning(self, "Error", message)
