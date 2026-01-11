from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QScrollArea)
from PyQt6.QtCore import Qt


class DevPacksPage(QWidget):
    """Dev Packs page - Install curated bundles of tools for specific workflows"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the dev packs page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Page title and description
        title = QLabel("Dev Packs")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel("Install curated bundles of tools for specific development workflows")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # Info banner
        info_banner = self.create_info_banner()
        layout.addWidget(info_banner)

        # Dev packs grid
        packs_scroll = self.create_packs_grid()
        layout.addWidget(packs_scroll)

    def create_info_banner(self):
        """Create info banner explaining dev packs"""
        banner = QFrame()
        banner.setObjectName("infoBanner")

        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 15, 20, 15)

        # Info icon
        icon = QLabel("ℹ️")
        icon.setStyleSheet("font-size: 24px;")
        banner_layout.addWidget(icon)

        # Info text
        text = QLabel(
            "Dev Packs bundle multiple tools together for common development workflows. Installing a pack will install all included tools.")
        text.setObjectName("infoBannerText")
        text.setWordWrap(True)
        banner_layout.addWidget(text)

        return banner

    def create_packs_grid(self):
        """Create scrollable grid of dev pack cards"""
        # Scroll area for packs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        grid = QGridLayout(scroll_content)
        grid.setSpacing(20)

        # Sample dev packs data: name, description, tools list, color, installed status
        packs_data = [
            ("Web Development", "Everything you need for modern web development",
             ["Node.js", "npm", "Git", "VS Code"], "#3B82F6", False),

            ("Python Data Science", "Tools for data analysis and machine learning",
             ["Python 3.12", "Jupyter", "pandas", "numpy"], "#10B981", True),

            ("DevOps Essentials", "Deploy and manage applications efficiently",
             ["Docker", "Kubernetes", "Terraform", "Ansible"], "#F59E0B", False),

            ("Mobile Development", "Build native and cross-platform mobile apps",
             ["Android Studio", "Flutter", "React Native", "Git"], "#8B5CF6", False),

            ("Database Stack", "Database management and administration tools",
             ["PostgreSQL", "MongoDB", "Redis", "MySQL"], "#EF4444", False),

            ("Go Development", "Complete setup for Go programming",
             ["Go", "gopls", "golangci-lint", "Docker"], "#06B6D4", False),
        ]

        # Create pack cards in grid (2 columns)
        row = 0
        col = 0
        for pack_name, pack_desc, tools, color, installed in packs_data:
            pack_card = self.create_pack_card(pack_name, pack_desc, tools, color, installed)
            grid.addWidget(pack_card, row, col)

            col += 1
            if col > 1:  # 2 columns per row
                col = 0
                row += 1

        scroll.setWidget(scroll_content)

        return scroll

    def create_pack_card(self, name, description, tools, color, installed):
        """Create an individual dev pack card"""
        card = QFrame()
        card.setObjectName("packCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Header with colored indicator
        header = QHBoxLayout()

        # Color indicator bar
        color_bar = QFrame()
        color_bar.setFixedSize(4, 40)
        color_bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")

        # Pack name
        name_label = QLabel(name)
        name_label.setObjectName("packName")

        header.addWidget(color_bar)
        header.addSpacing(15)
        header.addWidget(name_label)
        header.addStretch()

        layout.addLayout(header)

        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("packDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Tools list
        tools_label = QLabel("Includes:")
        tools_label.setObjectName("packToolsLabel")
        layout.addWidget(tools_label)

        tools_text = QLabel("• " + "\n• ".join(tools))
        tools_text.setObjectName("packToolsList")
        layout.addWidget(tools_text)

        layout.addStretch()

        # Install button
        btn_layout = QHBoxLayout()

        if installed:
            btn = QPushButton("✓ Installed")
            btn.setObjectName("installedButton")
        else:
            btn = QPushButton(f"Install Pack ({len(tools)} tools)")
            btn.setObjectName("installButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        return card