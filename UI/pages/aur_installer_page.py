# UI/pages/aur_installer_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QLineEdit, QScrollArea,
                             QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.aur_manager import AURManager


class AURWorker(QThread):
    """Worker thread for AUR operations"""
    finished = pyqtSignal(bool, str)
    search_results = pyqtSignal(list)

    def __init__(self, aur_manager, action, package_name=""):
        super().__init__()
        self.aur = aur_manager
        self.action = action
        self.package_name = package_name

    def run(self):
        try:
            if self.action == "install_helper":
                success, msg = self.aur.install_helper(self.package_name)
                self.finished.emit(success, msg)
            elif self.action == "remove_helper":
                success, msg = self.aur.remove_helper(self.package_name)
                self.finished.emit(success, msg)
            elif self.action == "search":
                results = self.aur.search_aur(self.package_name)
                self.search_results.emit(results)
            elif self.action == "install_package":
                success, msg = self.aur.install_package(self.package_name)
                self.finished.emit(success, msg)
            elif self.action == "remove_package":
                success, msg = self.aur.remove_package(self.package_name)
                self.finished.emit(success, msg)
        except Exception as e:
            self.finished.emit(False, str(e))


class AURInstallerPage(QWidget):
    """AUR Installer page - Search and install packages from Arch User Repository"""

    def __init__(self):
        super().__init__()
        self.aur = AURManager()
        self.helper_buttons = {}
        self.package_buttons = {}
        self.workers = []
        self.init_ui()

    def init_ui(self):
        """Initialize the AUR installer page UI"""
        # Create a scroll area for the entire page
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        # Page title and description
        title = QLabel("AUR Installer")
        title.setObjectName("pageTitle")
        self.main_layout.addWidget(title)

        desc = QLabel("Search and install packages from the Arch User Repository")
        desc.setObjectName("pageDescription")
        self.main_layout.addWidget(desc)

        # Check if Arch-based
        if not self.aur.is_arch_based:
            self.show_not_arch_message()
            scroll.setWidget(scroll_content)
            page_layout.addWidget(scroll)
            return

        # Warning banner
        warning_banner = self.create_warning_banner()
        self.main_layout.addWidget(warning_banner)

        # AUR Helper section
        helper_section = self.create_helper_section()
        self.main_layout.addWidget(helper_section)

        # Only show search and packages if helper is installed
        if self.aur.active_helper:
            # Stats row
            stats = self.create_stats_row()
            self.main_layout.addWidget(stats)

            # Search bar
            search_bar = self.create_search_bar()
            self.main_layout.addWidget(search_bar)

            # Packages list (no longer a scroll area, just a container)
            self.packages_container = self.create_packages_list()
            self.main_layout.addWidget(self.packages_container)
        else:
            no_helper = QLabel("Install an AUR helper above to search and install packages.")
            no_helper.setObjectName("pageDescription")
            no_helper.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(no_helper)

        self.main_layout.addStretch()
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

    def show_not_arch_message(self):
        """Show message for non-Arch systems"""
        message_frame = QFrame()
        message_frame.setObjectName("infoBanner")

        layout = QVBoxLayout(message_frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("🐧")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("AUR Not Available")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        desc = QLabel(
            "The Arch User Repository (AUR) is only available on Arch Linux and Arch-based distributions.\n\n"
            "Your current system does not appear to be Arch-based."
        )
        desc.setObjectName("pageDescription")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        self.main_layout.addWidget(message_frame)
        self.main_layout.addStretch()

    def create_warning_banner(self):
        """Create warning banner about AUR packages"""
        banner = QFrame()
        banner.setObjectName("warningBanner")

        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 15, 20, 15)

        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size: 24px;")
        banner_layout.addWidget(icon)

        text = QLabel(
            "AUR packages are user-produced content. Use at your own risk. "
            "Always review the PKGBUILD before installing."
        )
        text.setObjectName("warningBannerText")
        text.setWordWrap(True)
        banner_layout.addWidget(text)

        return banner

    def create_helper_section(self):
        """Create AUR helper management section"""
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Section title
        title_layout = QHBoxLayout()
        title = QLabel("🔧 AUR Helper")
        title.setObjectName("settingsSectionTitle")
        title_layout.addWidget(title)

        # Current helper status
        if self.aur.active_helper:
            status = QLabel(f"✓ {self.aur.active_helper} active")
            status.setObjectName("statusConnected")
        else:
            status = QLabel("No helper installed")
            status.setObjectName("statusOS")

        title_layout.addStretch()
        title_layout.addWidget(status)
        layout.addLayout(title_layout)

        desc = QLabel("An AUR helper is required to search and install packages from the AUR.")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # Helper cards
        helpers_layout = QHBoxLayout()
        helpers_layout.setSpacing(15)

        for helper_name, helper_info in self.aur.SUPPORTED_HELPERS.items():
            card = self.create_helper_card(helper_name, helper_info)
            helpers_layout.addWidget(card)

        helpers_layout.addStretch()
        layout.addLayout(helpers_layout)

        return section

    def create_helper_card(self, helper_name, helper_info):
        """Create a card for an AUR helper"""
        card = QFrame()
        card.setObjectName("toolCard")
        card.setFixedWidth(250)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Helper name
        name = QLabel(helper_name)
        name.setObjectName("toolName")
        layout.addWidget(name)

        # Description
        desc = QLabel(helper_info["description"])
        desc.setObjectName("toolDescription")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        # Install/Remove button
        installed = self.aur.is_helper_installed(helper_name)

        if installed:
            btn = QPushButton("✓ Installed")
            btn.setObjectName("installedButton")
            btn.clicked.connect(lambda: self.on_remove_helper(helper_name, btn))
        else:
            btn = QPushButton("Install")
            btn.setObjectName("installButton")
            btn.clicked.connect(lambda: self.on_install_helper(helper_name, btn))

        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.helper_buttons[helper_name] = btn
        layout.addWidget(btn)

        return card

    def on_install_helper(self, helper_name, button):
        """Handle helper installation"""
        reply = QMessageBox.question(
            self, "Install AUR Helper",
            f"Do you want to install {helper_name}?\n\n"
            "This will compile the helper from source.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            button.setText("Installing...")
            button.setEnabled(False)

            worker = AURWorker(self.aur, "install_helper", helper_name)
            worker.finished.connect(
                lambda success, msg: self.on_helper_operation_finished(success, msg, helper_name, button, "install")
            )
            self.workers.append(worker)
            worker.start()

    def on_remove_helper(self, helper_name, button):
        """Handle helper removal"""
        reply = QMessageBox.question(
            self, "Remove AUR Helper",
            f"Are you sure you want to remove {helper_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            button.setText("Removing...")
            button.setEnabled(False)

            worker = AURWorker(self.aur, "remove_helper", helper_name)
            worker.finished.connect(
                lambda success, msg: self.on_helper_operation_finished(success, msg, helper_name, button, "remove")
            )
            self.workers.append(worker)
            worker.start()

    def on_helper_operation_finished(self, success, message, helper_name, button, action):
        """Handle helper operation completion"""
        button.setEnabled(True)

        if success:
            QMessageBox.information(self, "Success", message)
            # Refresh the entire page to update UI state
            self.refresh_page()
        else:
            if action == "install":
                button.setText("Install")
                button.setObjectName("installButton")
            else:
                button.setText("✓ Installed")
                button.setObjectName("installedButton")
            button.setStyle(button.style())
            QMessageBox.warning(self, "Error", message)

    def refresh_page(self):
        """Refresh the entire page"""
        # Clear the parent layout
        parent_layout = self.layout()
        if parent_layout:
            while parent_layout.count():
                item = parent_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Reinitialize
        self.aur = AURManager()
        self.helper_buttons = {}
        self.package_buttons = {}
        self.init_ui()

    def create_search_bar(self):
        """Create search input with search button"""
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("🔍 Search AUR packages...")
        self.search_input.setFixedHeight(45)
        self.search_input.returnPressed.connect(self.on_search)

        self.search_btn = QPushButton("Search")
        self.search_btn.setObjectName("searchButton")
        self.search_btn.setFixedWidth(100)
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.clicked.connect(self.on_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        return search_container

    def on_search(self):
        """Handle search button click"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Search", "Please enter a search term.")
            return

        self.search_btn.setText("Searching...")
        self.search_btn.setEnabled(False)

        worker = AURWorker(self.aur, "search", query)
        worker.search_results.connect(self.on_search_results)
        self.workers.append(worker)
        worker.start()

    def on_search_results(self, results):
        """Handle search results"""
        self.search_btn.setText("Search")
        self.search_btn.setEnabled(True)

        # Update packages list
        self.update_packages_list(results)

    def update_packages_list(self, packages):
        """Update the packages list with search results"""
        self.main_layout.removeWidget(self.packages_container)
        self.packages_container.deleteLater()

        self.packages_container = self.create_packages_list(packages)
        # Insert before the stretch
        self.main_layout.insertWidget(self.main_layout.count() - 1, self.packages_container)

    def create_stats_row(self):
        """Create statistics row showing AUR info"""
        stats_container = QFrame()
        stats_container.setObjectName("aurStatsContainer")

        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(20, 15, 20, 15)
        stats_layout.setSpacing(40)

        # Active helper
        helper_layout = QVBoxLayout()
        helper_label = QLabel("Active Helper")
        helper_label.setObjectName("aurStatLabel")
        helper_value = QLabel(self.aur.active_helper or "None")
        helper_value.setObjectName("aurStatValue")
        helper_layout.addWidget(helper_label)
        helper_layout.addWidget(helper_value)

        # Installed from AUR
        installed_packages = self.aur.get_installed_aur_packages()
        installed_layout = QVBoxLayout()
        installed_label = QLabel("Installed from AUR")
        installed_label.setObjectName("aurStatLabel")
        installed_value = QLabel(str(len(installed_packages)))
        installed_value.setObjectName("aurStatValue")
        installed_layout.addWidget(installed_label)
        installed_layout.addWidget(installed_value)

        stats_layout.addLayout(helper_layout)
        stats_layout.addLayout(installed_layout)
        stats_layout.addStretch()

        return stats_container

    def create_packages_list(self, packages=None):
        """Create list of AUR packages (no scroll - parent handles scrolling)"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        if packages is None:
            # Show placeholder
            placeholder = QLabel("Search for packages to install from the AUR")
            placeholder.setObjectName("pageDescription")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(placeholder)
            return container

        if not packages:
            no_results = QLabel("No packages found")
            no_results.setObjectName("pageDescription")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_results)
            return container

        for pkg in packages:
            item = self.create_package_item(
                pkg.get("name", ""),
                pkg.get("version", ""),
                pkg.get("description", ""),
                pkg.get("votes", 0),
                pkg.get("popularity", 0)
            )
            layout.addWidget(item)

        return container

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
        desc_label = QLabel(description if description else "No description available")
        desc_label.setObjectName("aurPackageDescription")
        desc_label.setWordWrap(True)

        # Stats
        stats_layout = QHBoxLayout()
        votes_label = QLabel(f"👍 {votes} votes")
        votes_label.setObjectName("aurPackageStat")
        popularity_label = QLabel(f"📊 {popularity:.2f}")
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

        installed = self.aur.is_package_installed(name)

        if installed:
            install_btn = QPushButton("✓ Installed")
            install_btn.setObjectName("installedButton")
            install_btn.clicked.connect(lambda: self.on_remove_package(name, install_btn))
        else:
            install_btn = QPushButton("Install")
            install_btn.setObjectName("installButton")
            install_btn.clicked.connect(lambda: self.on_install_package(name, install_btn))

        install_btn.setFixedWidth(100)
        install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.package_buttons[name] = install_btn

        buttons_layout.addWidget(install_btn)
        layout.addLayout(buttons_layout)

        return item

    def on_install_package(self, package_name, button):
        """Handle package installation"""
        button.setText("Installing...")
        button.setEnabled(False)

        worker = AURWorker(self.aur, "install_package", package_name)
        worker.finished.connect(
            lambda success, msg: self.on_package_operation_finished(success, msg, package_name, button, "install")
        )
        self.workers.append(worker)
        worker.start()

    def on_remove_package(self, package_name, button):
        """Handle package removal"""
        reply = QMessageBox.question(
            self, "Remove Package",
            f"Are you sure you want to remove {package_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            button.setText("Removing...")
            button.setEnabled(False)

            worker = AURWorker(self.aur, "remove_package", package_name)
            worker.finished.connect(
                lambda success, msg: self.on_package_operation_finished(success, msg, package_name, button, "remove")
            )
            self.workers.append(worker)
            worker.start()

    def on_package_operation_finished(self, success, message, package_name, button, action):
        """Handle package operation completion"""
        button.setEnabled(True)

        if success:
            if action == "install":
                button.setText("✓ Installed")
                button.setObjectName("installedButton")
                button.clicked.disconnect()
                button.clicked.connect(lambda: self.on_remove_package(package_name, button))
            else:
                button.setText("Install")
                button.setObjectName("installButton")
                button.clicked.disconnect()
                button.clicked.connect(lambda: self.on_install_package(package_name, button))

            button.setStyle(button.style())
            QMessageBox.information(self, "Success", message)
        else:
            if action == "install":
                button.setText("Install")
            else:
                button.setText("✓ Installed")
            QMessageBox.warning(self, "Error", message)
