from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt


class AURInstallerPage(QWidget):
    """AUR Installer page - Search and install packages from Arch User Repository"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the AUR installer page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Page title and description
        title = QLabel("AUR Installer")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel("Search and install packages from the Arch User Repository")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # Warning banner
        warning_banner = self.create_warning_banner()
        layout.addWidget(warning_banner)

        # Search bar with advanced button
        search_bar = self.create_search_bar()
        layout.addWidget(search_bar)

        # Stats row
        stats_row = self.create_stats_row()
        layout.addWidget(stats_row)

        # Packages list
        packages_scroll = self.create_packages_list()
        layout.addWidget(packages_scroll)

    def create_warning_banner(self):
        """Create warning banner about AUR packages"""
        banner = QFrame()
        banner.setObjectName("warningBanner")

        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 15, 20, 15)

        # Warning icon
        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size: 24px;")
        banner_layout.addWidget(icon)

        # Warning text
        text = QLabel(
            "AUR packages are user-produced content. Use at your own risk and always review PKGBUILDs before installing.")
        text.setObjectName("warningBannerText")
        text.setWordWrap(True)
        banner_layout.addWidget(text)

        return banner

    def create_search_bar(self):
        """Create search input with search button"""
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)

        # Search input field
        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("🔍 Search AUR packages...")
        search_input.setFixedHeight(45)

        # Search button
        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        search_btn.setFixedWidth(100)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        search_layout.addWidget(search_input)
        search_layout.addWidget(search_btn)

        return search_container

    def create_stats_row(self):
        """Create statistics row showing AUR info"""
        stats_container = QFrame()
        stats_container.setObjectName("aurStatsContainer")

        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(20, 15, 20, 15)
        stats_layout.setSpacing(40)

        # Total packages stat
        total_layout = QVBoxLayout()
        total_label = QLabel("Total Packages")
        total_label.setObjectName("aurStatLabel")
        total_value = QLabel("85,247")
        total_value.setObjectName("aurStatValue")
        total_layout.addWidget(total_label)
        total_layout.addWidget(total_value)

        # Installed stat
        installed_layout = QVBoxLayout()
        installed_label = QLabel("Installed from AUR")
        installed_label.setObjectName("aurStatLabel")
        installed_value = QLabel("3")
        installed_value.setObjectName("aurStatValue")
        installed_layout.addWidget(installed_label)
        installed_layout.addWidget(installed_value)

        # Last updated stat
        updated_layout = QVBoxLayout()
        updated_label = QLabel("Last Updated")
        updated_label.setObjectName("aurStatLabel")
        updated_value = QLabel("15 min ago")
        updated_value.setObjectName("aurStatValue")
        updated_layout.addWidget(updated_label)
        updated_layout.addWidget(updated_value)

        stats_layout.addLayout(total_layout)
        stats_layout.addLayout(installed_layout)
        stats_layout.addLayout(updated_layout)
        stats_layout.addStretch()

        return stats_container

    def create_packages_list(self):
        """Create scrollable list of AUR packages"""
        # Scroll area for packages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(12)

        # Sample AUR packages data: name, version, description, votes, popularity
        packages_data = [
            ("visual-studio-code-bin", "1.85.1-1", "Visual Studio Code (binary)", "12,453", "9.87"),
            ("google-chrome", "120.0.6099.109-1", "The popular web browser by Google", "8,921", "8.54"),
            ("spotify", "1.2.31.1205-1", "A proprietary music streaming service", "7,234", "7.92"),
            ("slack-desktop", "4.36.134-1", "Slack Desktop for Linux", "5,678", "6.45"),
            ("zoom", "5.16.10.668-1", "Video conferencing and web conferencing service", "4,123", "5.23"),
            ("discord", "0.0.40-1", "All-in-one voice and text chat", "9,876", "8.91"),
        ]

        # Create package items
        for pkg_name, version, description, votes, popularity in packages_data:
            pkg_item = self.create_package_item(pkg_name, version, description, votes, popularity)
            layout.addWidget(pkg_item)

        layout.addStretch()

        scroll.setWidget(scroll_content)

        return scroll

    def create_package_item(self, name, version, description, votes, popularity):
        """Create an individual package list item"""
        item = QFrame()
        item.setObjectName("aurPackageItem")

        layout = QHBoxLayout(item)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Left side - package info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        # Package name and version
        name_layout = QHBoxLayout()
        name_label = QLabel(name)
        name_label.setObjectName("aurPackageName")
        version_label = QLabel(version)
        version_label.setObjectName("aurPackageVersion")
        name_layout.addWidget(name_label)
        name_layout.addWidget(version_label)
        name_layout.addStretch()

        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("aurPackageDescription")

        # Stats (votes and popularity)
        stats_layout = QHBoxLayout()
        votes_label = QLabel(f"👍 {votes} votes")
        votes_label.setObjectName("aurPackageStat")
        popularity_label = QLabel(f"📊 {popularity}% popularity")
        popularity_label.setObjectName("aurPackageStat")
        stats_layout.addWidget(votes_label)
        stats_layout.addSpacing(20)
        stats_layout.addWidget(popularity_label)
        stats_layout.addStretch()

        info_layout.addLayout(name_layout)
        info_layout.addWidget(desc_label)
        info_layout.addLayout(stats_layout)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Right side - action buttons
        buttons_layout = QVBoxLayout()

        install_btn = QPushButton("Install")
        install_btn.setObjectName("installButton")
        install_btn.setFixedWidth(100)
        install_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        info_btn = QPushButton("More Info")
        info_btn.setObjectName("infoButton")
        info_btn.setFixedWidth(100)
        info_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        buttons_layout.addWidget(install_btn)
        buttons_layout.addWidget(info_btn)

        layout.addLayout(buttons_layout)

        return item