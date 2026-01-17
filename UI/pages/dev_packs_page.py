# UI/pages/dev_packs_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QScrollArea,
                             QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.package_manager import PackageManager


class PackInstallWorker(QThread):
    """Worker thread for installing/removing pack packages"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, package_manager, packages, action="install"):
        super().__init__()
        self.pm = package_manager
        self.packages = packages
        self.action = action

    def run(self):
        try:
            total = len(self.packages)
            success_count = 0
            failed_packages = []

            for i, package in enumerate(self.packages):
                self.progress.emit(int((i / total) * 100), package)

                if self.action == "install":
                    if not self.pm.is_installed(package):
                        if self.pm.install(package):
                            success_count += 1
                        else:
                            failed_packages.append(package)
                    else:
                        success_count += 1
                elif self.action == "remove":
                    if self.pm.is_installed(package):
                        if self.pm.remove(package):
                            success_count += 1
                        else:
                            failed_packages.append(package)
                    else:
                        success_count += 1

            self.progress.emit(100, "Done")

            if failed_packages:
                msg = f"Completed with {len(failed_packages)} failures: {', '.join(failed_packages)}"
                self.finished.emit(False, msg)
            else:
                action_word = "installed" if self.action == "install" else "removed"
                self.finished.emit(True, f"Successfully {action_word} {success_count} packages")

        except Exception as e:
            self.finished.emit(False, str(e))


class DevPacksPage(QWidget):
    """Dev Packs page - Install curated sets of development tools"""

    def __init__(self):
        super().__init__()
        self.pm = PackageManager()
        self.pack_buttons = {}
        self.workers = []
        self.init_ui()

    def get_packs_data(self):
        """Get development packs data"""
        packs = [
            {
                "name": "Web Development",
                "description": "Essential tools for building modern web applications",
                "icon": "🌐",
                "packages": ["nodejs", "git", "nginx", "redis", "curl"],
                "color": "#3B82F6"
            },
            {
                "name": "Python Development",
                "description": "Complete Python development environment with essential tools",
                "icon": "🐍",
                "packages": ["python3", "python3-pip", "python3-venv", "git", "vim"],
                "color": "#10B981"
            },
            {
                "name": "DevOps Essentials",
                "description": "Tools for containerization, automation, and deployment",
                "icon": "🐳",
                "packages": ["docker", "git", "curl", "wget", "htop", "tmux"],
                "color": "#8B5CF6"
            },
            {
                "name": "Database Stack",
                "description": "Popular database systems for development and testing",
                "icon": "🗄️",
                "packages": ["postgresql", "redis", "mysql-server"],
                "color": "#F59E0B"
            },
            {
                "name": "System Tools",
                "description": "Essential system utilities for Linux development",
                "icon": "🔧",
                "packages": ["htop", "tmux", "vim", "curl", "wget", "git"],
                "color": "#EF4444"
            },
            {
                "name": "Full Stack",
                "description": "Comprehensive set for full-stack web development",
                "icon": "🚀",
                "packages": ["nodejs", "python3", "git", "docker", "postgresql", "redis", "nginx"],
                "color": "#EC4899"
            },
        ]
        return packs

    def init_ui(self):
        """Initialize the dev packs page UI"""
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
        title = QLabel("Development Packs")
        title.setObjectName("pageTitle")
        self.main_layout.addWidget(title)

        desc = QLabel("Install curated sets of development tools with one click")
        desc.setObjectName("pageDescription")
        self.main_layout.addWidget(desc)

        # Info banner
        info_banner = self.create_info_banner()
        self.main_layout.addWidget(info_banner)

        # Packs grid container
        self.packs_container = QWidget()
        self.packs_layout = QVBoxLayout(self.packs_container)
        self.packs_layout.setContentsMargins(0, 0, 0, 0)
        self.build_packs_grid()
        self.main_layout.addWidget(self.packs_container)

        self.main_layout.addStretch()
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

    def create_info_banner(self):
        """Create informational banner"""
        banner = QFrame()
        banner.setObjectName("infoBanner")

        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 15, 20, 15)

        icon = QLabel("💡")
        icon.setStyleSheet("font-size: 24px;")
        banner_layout.addWidget(icon)

        text = QLabel(
            "Development packs are pre-configured sets of tools commonly used together. "
            "Installing a pack will install all included packages that aren't already on your system."
        )
        text.setObjectName("infoBannerText")
        text.setWordWrap(True)
        banner_layout.addWidget(text)

        return banner

    def build_packs_grid(self):
        """Build the packs grid widget"""
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)

        packs_data = self.get_packs_data()

        row, col = 0, 0
        for pack in packs_data:
            pack_card = self.create_pack_card(pack)
            grid.addWidget(pack_card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.packs_layout.addWidget(grid_widget)

    def create_pack_card(self, pack):
        """Create a pack card with package list and install button"""
        card = QFrame()
        card.setObjectName("packCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        header = QHBoxLayout()
        icon_label = QLabel(pack["icon"])
        icon_label.setStyleSheet("font-size: 36px;")
        name_label = QLabel(pack["name"])
        name_label.setObjectName("packName")
        header.addWidget(icon_label)
        header.addWidget(name_label)
        header.addStretch()
        layout.addLayout(header)

        desc_label = QLabel(pack["description"])
        desc_label.setObjectName("packDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        tools_label = QLabel("Included packages:")
        tools_label.setObjectName("packToolsLabel")
        layout.addWidget(tools_label)

        packages_text = self.format_packages_list(pack["packages"])
        tools_list = QLabel(packages_text)
        tools_list.setObjectName("packToolsList")
        tools_list.setWordWrap(True)
        layout.addWidget(tools_list)

        layout.addStretch()

        progress_bar = QProgressBar()
        progress_bar.setVisible(False)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #252A3A;
                border: none;
                border-radius: 4px;
                height: 20px;
                text-align: center;
                color: #FFFFFF;
            }}
            QProgressBar::chunk {{
                background-color: {pack["color"]};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress_bar)

        buttons_layout = QHBoxLayout()
        installed_count = sum(1 for pkg in pack["packages"] if self.pm.is_installed(pkg))
        total_count = len(pack["packages"])

        if installed_count == total_count:
            install_btn = QPushButton("✓ All Installed")
            install_btn.setObjectName("installedButton")
        elif installed_count > 0:
            install_btn = QPushButton(f"Install ({total_count - installed_count} remaining)")
            install_btn.setObjectName("installButton")
        else:
            install_btn = QPushButton("Install Pack")
            install_btn.setObjectName("installButton")

        install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        install_btn.clicked.connect(
            lambda: self.on_install_pack(pack["name"], pack["packages"], install_btn, progress_bar)
        )

        remove_btn = QPushButton("Remove")
        remove_btn.setObjectName("infoButton")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(
            lambda: self.on_remove_pack(pack["name"], pack["packages"], install_btn, progress_bar)
        )

        self.pack_buttons[pack["name"]] = {
            "install": install_btn,
            "remove": remove_btn,
            "progress": progress_bar,
            "packages": pack["packages"]
        }

        buttons_layout.addWidget(install_btn)
        buttons_layout.addWidget(remove_btn)
        layout.addLayout(buttons_layout)

        return card

    def format_packages_list(self, packages):
        formatted = []
        for pkg in packages:
            if self.pm.is_installed(pkg):
                formatted.append(f"✓ {pkg}")
            else:
                formatted.append(f"○ {pkg}")
        return "  •  ".join(formatted)

    def on_install_pack(self, pack_name, packages, button, progress_bar):
        to_install = [pkg for pkg in packages if not self.pm.is_installed(pkg)]
        if not to_install:
            QMessageBox.information(self, "Already Installed", f"All packages in {pack_name} are already installed.")
            return

        reply = QMessageBox.question(self, "Install Pack",
            f"Install {len(to_install)} packages from {pack_name}?\n\nPackages: {', '.join(to_install)}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            button.setEnabled(False)
            button.setText("Installing...")
            progress_bar.setVisible(True)
            progress_bar.setValue(0)

            worker = PackInstallWorker(self.pm, to_install, "install")
            worker.progress.connect(lambda val, pkg: self.on_progress(val, pkg, progress_bar))
            worker.finished.connect(lambda success, msg: self.on_pack_finished(success, msg, pack_name, button, progress_bar))
            self.workers.append(worker)
            worker.start()

    def on_remove_pack(self, pack_name, packages, button, progress_bar):
        to_remove = [pkg for pkg in packages if self.pm.is_installed(pkg)]
        if not to_remove:
            QMessageBox.information(self, "Not Installed", f"No packages from {pack_name} are installed.")
            return

        reply = QMessageBox.question(self, "Remove Pack",
            f"Remove {len(to_remove)} packages from {pack_name}?\n\nPackages: {', '.join(to_remove)}\n\n⚠️ This may affect other applications.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            button.setEnabled(False)
            button.setText("Removing...")
            progress_bar.setVisible(True)
            progress_bar.setValue(0)

            worker = PackInstallWorker(self.pm, to_remove, "remove")
            worker.progress.connect(lambda val, pkg: self.on_progress(val, pkg, progress_bar))
            worker.finished.connect(lambda success, msg: self.on_pack_finished(success, msg, pack_name, button, progress_bar))
            self.workers.append(worker)
            worker.start()

    def on_progress(self, value, package, progress_bar):
        progress_bar.setValue(value)
        progress_bar.setFormat(f"{value}% - {package}")

    def on_pack_finished(self, success, message, pack_name, button, progress_bar):
        button.setEnabled(True)
        progress_bar.setVisible(False)

        pack_data = self.pack_buttons.get(pack_name)
        if pack_data:
            packages = pack_data["packages"]
            installed_count = sum(1 for pkg in packages if self.pm.is_installed(pkg))
            total_count = len(packages)

            if installed_count == total_count:
                button.setText("✓ All Installed")
                button.setObjectName("installedButton")
            elif installed_count > 0:
                button.setText(f"Install ({total_count - installed_count} remaining)")
                button.setObjectName("installButton")
            else:
                button.setText("Install Pack")
                button.setObjectName("installButton")
            button.setStyle(button.style())

        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Warning", message)
