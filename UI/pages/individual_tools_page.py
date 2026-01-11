from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt


class IndividualToolsPage(QWidget):
    """Individual Tools page - Browse and install development tools one by one"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the individual tools page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Page title and description
        title = QLabel("Individual Tools")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel("Browse and install development tools individually")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # Search bar
        search_bar = self.create_search_bar()
        layout.addWidget(search_bar)

        # Category filters
        filters = self.create_filters()
        layout.addWidget(filters)

        # Tools grid - scrollable area
        tools_scroll = self.create_tools_grid()
        layout.addWidget(tools_scroll)

    def create_search_bar(self):
        """Create search input field"""
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)

        # Search input field
        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("🔍 Search tools...")
        search_input.setFixedHeight(45)

        search_layout.addWidget(search_input)

        return search_container

    def create_filters(self):
        """Create category filter buttons"""
        filter_container = QWidget()
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)

        # Filter button categories
        categories = ["All", "Languages", "Version Control", "Databases", "Web Dev", "DevOps"]

        for i, category in enumerate(categories):
            btn = QPushButton(category)
            # First button is active by default
            if i == 0:
                btn.setObjectName("filterButtonActive")
            else:
                btn.setObjectName("filterButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            filter_layout.addWidget(btn)

        filter_layout.addStretch()

        return filter_container

    def create_tools_grid(self):
        """Create scrollable grid of tool cards"""
        # Scroll area for tools
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        grid = QGridLayout(scroll_content)
        grid.setSpacing(20)

        # Sample tools data: name, description, icon, installed status
        tools_data = [
            ("Python 3.12", "High-level programming language", "🐍", True),
            ("Node.js", "JavaScript runtime environment", "📗", True),
            ("Git", "Distributed version control system", "📝", True),
            ("Docker", "Container platform", "🐳", False),
            ("PostgreSQL", "Relational database system", "🐘", False),
            ("VS Code", "Code editor", "📝", True),
            ("Nginx", "Web server", "🌐", False),
            ("Redis", "In-memory data store", "🔴", False),
            ("MongoDB", "NoSQL database", "🍃", False),
        ]

        # Create tool cards in grid (3 columns)
        row = 0
        col = 0
        for tool_name, tool_desc, icon, installed in tools_data:
            tool_card = self.create_tool_card(tool_name, tool_desc, icon, installed)
            grid.addWidget(tool_card, row, col)

            col += 1
            if col > 2:  # 3 columns per row
                col = 0
                row += 1

        scroll.setWidget(scroll_content)

        return scroll

    def create_tool_card(self, name, description, icon, installed):
        """Create an individual tool card"""
        card = QFrame()
        card.setObjectName("toolCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Header with icon and name
        header = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")

        name_label = QLabel(name)
        name_label.setObjectName("toolName")

        header.addWidget(icon_label)
        header.addWidget(name_label)
        header.addStretch()

        layout.addLayout(header)

        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("toolDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()

        # Install/Installed button
        if installed:
            btn = QPushButton("✓ Installed")
            btn.setObjectName("installedButton")
        else:
            btn = QPushButton("Install")
            btn.setObjectName("installButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(btn)

        return card