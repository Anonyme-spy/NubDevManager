from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame)
from PyQt6.QtCore import Qt


class HomePage(QWidget):
    """Home page - Welcome screen with overview cards and quick stats"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the home page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Welcome banner with gradient background
        banner = self.create_banner()
        layout.addWidget(banner)

        # Grid with feature cards
        cards_grid = self.create_cards_grid()
        layout.addWidget(cards_grid)

        # Quick stats section
        stats = self.create_quick_stats()
        layout.addWidget(stats)

        layout.addStretch()

    def create_banner(self):
        """Create the welcome banner with call-to-action"""
        banner = QFrame()
        banner.setObjectName("banner")

        layout = QHBoxLayout(banner)
        layout.setContentsMargins(40, 40, 40, 40)

        # Left side - text content
        text_layout = QVBoxLayout()

        welcome_title = QLabel("Welcome to Dev Manager")
        welcome_title.setObjectName("bannerTitle")

        welcome_text = QLabel(
            "Your all-in-one development environment setup tool for Linux. Install and manage\ndevelopment tools with ease.")
        welcome_text.setObjectName("bannerText")

        get_started_btn = QPushButton("Get Started")
        get_started_btn.setObjectName("getStartedButton")
        get_started_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        get_started_btn.setFixedWidth(120)

        text_layout.addWidget(welcome_title)
        text_layout.addWidget(welcome_text)
        text_layout.addSpacing(15)
        text_layout.addWidget(get_started_btn)
        text_layout.addStretch()

        layout.addLayout(text_layout)
        layout.addStretch()

        # Right side - Tux penguin icon
        tux_label = QLabel("🐧")
        tux_label.setObjectName("tuxIcon")
        tux_label.setStyleSheet("font-size: 80px;")
        layout.addWidget(tux_label, alignment=Qt.AlignmentFlag.AlignRight)

        return banner

    def create_cards_grid(self):
        """Create grid layout with three feature cards"""
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)

        # Define card data: icon, title, description, action text, color
        cards_data = [
            ("🔧", "Individual Tools", "Install specific development tools one by one", "Explore →", "#4A90E2"),
            ("📦", "Dev Packs", "Install curated bundles for specific workflows", "Browse →", "#2ECC71"),
            ("📥", "AUR Installer", "Access Arch User Repository packages", "Search →", "#9B59B6")
        ]

        # Create and add cards to grid
        for i, (icon, title, desc, action, color) in enumerate(cards_data):
            card = self.create_card(icon, title, desc, action, color)
            grid.addWidget(card, 0, i)

        return grid_widget

    def create_card(self, icon, title, desc, action, color):
        """Create an individual feature card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Icon with colored background
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 32px; background-color: {color}; padding: 12px; border-radius: 8px;")
        icon_label.setFixedSize(56, 56)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card title
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        # Card description
        desc_label = QLabel(desc)
        desc_label.setObjectName("cardDesc")
        desc_label.setWordWrap(True)

        # Action link
        action_label = QLabel(action)
        action_label.setObjectName("cardAction")
        action_label.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(action_label)

        return card

    def create_quick_stats(self):
        """Create the quick stats section with metrics"""
        stats = QFrame()
        stats.setObjectName("statsCard")

        layout = QVBoxLayout(stats)
        layout.setContentsMargins(30, 25, 30, 25)

        # Section title
        title = QLabel("Quick Stats")
        title.setObjectName("statsTitle")
        layout.addWidget(title)

        # Stats grid - 4 columns with label and value
        stats_grid = QWidget()
        grid = QGridLayout(stats_grid)
        grid.setSpacing(40)

        # Define stats data: label, value
        stats_data = [
            ("Installed Tools", "12"),
            ("Available Tools", "48"),
            ("Dev Packs", "8"),
            ("Last Updated", "2h")
        ]

        # Create stat columns
        for i, (label, value) in enumerate(stats_data):
            col = QVBoxLayout()

            label_widget = QLabel(label)
            label_widget.setObjectName("statLabel")

            value_widget = QLabel(value)
            value_widget.setObjectName("statValue")

            col.addWidget(label_widget)
            col.addWidget(value_widget)

            grid.addLayout(col, 0, i)

        layout.addWidget(stats_grid)

        return stats