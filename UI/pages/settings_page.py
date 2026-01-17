# UI/pages/settings_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QCheckBox, QComboBox,
                             QLineEdit, QScrollArea, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
import json
import os


class SettingsPage(QWidget):
    """Settings page - Configure application preferences"""

    def __init__(self):
        super().__init__()
        self.settings_file = os.path.expanduser("~/.config/dev_manager/settings.json")
        self.settings = self.load_settings()
        self.init_ui()

    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            "theme": "Dark",
            "auto_update_check": True,
            "confirm_installations": True,
            "confirm_removals": True,
            "keep_logs_days": 30,
            "default_helper": "yay",
            "parallel_downloads": 5,
            "show_aur_warnings": True,
            "log_level": "Info",
            "custom_install_path": "",
            "auto_clean_cache": False,
        }

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
        except Exception:
            pass

        return default_settings

    def save_settings(self):
        """Save settings to file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception:
            return False

    def init_ui(self):
        """Initialize the settings page UI"""
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        # Page title
        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        self.main_layout.addWidget(title)

        desc = QLabel("Configure application preferences and behavior")
        desc.setObjectName("pageDescription")
        self.main_layout.addWidget(desc)

        # General Settings Section
        general_section = self.create_general_section()
        self.main_layout.addWidget(general_section)

        # Package Manager Section
        package_section = self.create_package_section()
        self.main_layout.addWidget(package_section)

        # AUR Settings Section
        aur_section = self.create_aur_section()
        self.main_layout.addWidget(aur_section)

        # Logs Section
        logs_section = self.create_logs_section()
        self.main_layout.addWidget(logs_section)

        # Action buttons
        actions = self.create_actions()
        self.main_layout.addWidget(actions)

        self.main_layout.addStretch()
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

    def create_general_section(self):
        """Create general settings section"""
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("⚙️ General")
        title.setObjectName("settingsSectionTitle")
        layout.addWidget(title)

        # Theme selection
        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme")
        theme_label.setObjectName("settingsLabel")
        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("settingsCombo")
        self.theme_combo.addItems(["Dark", "Light", "System"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "Dark"))
        self.theme_combo.setFixedWidth(200)
        theme_row.addWidget(theme_label)
        theme_row.addStretch()
        theme_row.addWidget(self.theme_combo)
        layout.addLayout(theme_row)

        # Auto update check
        self.auto_update_check = QCheckBox("Check for updates on startup")
        self.auto_update_check.setObjectName("settingsCheckbox")
        self.auto_update_check.setChecked(self.settings.get("auto_update_check", True))
        layout.addWidget(self.auto_update_check)

        return section

    def create_package_section(self):
        """Create package manager settings section"""
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("📦 Package Manager")
        title.setObjectName("settingsSectionTitle")
        layout.addWidget(title)

        # Confirm installations
        self.confirm_install = QCheckBox("Confirm before installing packages")
        self.confirm_install.setObjectName("settingsCheckbox")
        self.confirm_install.setChecked(self.settings.get("confirm_installations", True))
        layout.addWidget(self.confirm_install)

        # Confirm removals
        self.confirm_remove = QCheckBox("Confirm before removing packages")
        self.confirm_remove.setObjectName("settingsCheckbox")
        self.confirm_remove.setChecked(self.settings.get("confirm_removals", True))
        layout.addWidget(self.confirm_remove)

        # Auto clean cache
        self.auto_clean = QCheckBox("Automatically clean package cache")
        self.auto_clean.setObjectName("settingsCheckbox")
        self.auto_clean.setChecked(self.settings.get("auto_clean_cache", False))
        layout.addWidget(self.auto_clean)

        # Parallel downloads
        parallel_row = QHBoxLayout()
        parallel_label = QLabel("Parallel downloads")
        parallel_label.setObjectName("settingsLabel")
        self.parallel_combo = QComboBox()
        self.parallel_combo.setObjectName("settingsCombo")
        self.parallel_combo.addItems(["1", "3", "5", "10"])
        self.parallel_combo.setCurrentText(str(self.settings.get("parallel_downloads", 5)))
        self.parallel_combo.setFixedWidth(200)
        parallel_row.addWidget(parallel_label)
        parallel_row.addStretch()
        parallel_row.addWidget(self.parallel_combo)
        layout.addLayout(parallel_row)

        return section

    def create_aur_section(self):
        """Create AUR settings section"""
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("📥 AUR Settings")
        title.setObjectName("settingsSectionTitle")
        layout.addWidget(title)

        # Default AUR helper
        helper_row = QHBoxLayout()
        helper_label = QLabel("Default AUR helper")
        helper_label.setObjectName("settingsLabel")
        self.helper_combo = QComboBox()
        self.helper_combo.setObjectName("settingsCombo")
        self.helper_combo.addItems(["yay", "paru", "trizen"])
        self.helper_combo.setCurrentText(self.settings.get("default_helper", "yay"))
        self.helper_combo.setFixedWidth(200)
        helper_row.addWidget(helper_label)
        helper_row.addStretch()
        helper_row.addWidget(self.helper_combo)
        layout.addLayout(helper_row)

        # Show AUR warnings
        self.show_warnings = QCheckBox("Show AUR safety warnings")
        self.show_warnings.setObjectName("settingsCheckbox")
        self.show_warnings.setChecked(self.settings.get("show_aur_warnings", True))
        layout.addWidget(self.show_warnings)

        return section

    def create_logs_section(self):
        """Create logs settings section"""
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("📋 Logs")
        title.setObjectName("settingsSectionTitle")
        layout.addWidget(title)

        # Log level
        level_row = QHBoxLayout()
        level_label = QLabel("Log level")
        level_label.setObjectName("settingsLabel")
        self.level_combo = QComboBox()
        self.level_combo.setObjectName("settingsCombo")
        self.level_combo.addItems(["Debug", "Info", "Warning", "Error"])
        self.level_combo.setCurrentText(self.settings.get("log_level", "Info"))
        self.level_combo.setFixedWidth(200)
        level_row.addWidget(level_label)
        level_row.addStretch()
        level_row.addWidget(self.level_combo)
        layout.addLayout(level_row)

        # Keep logs days
        days_row = QHBoxLayout()
        days_label = QLabel("Keep logs for (days)")
        days_label.setObjectName("settingsLabel")
        self.days_combo = QComboBox()
        self.days_combo.setObjectName("settingsCombo")
        self.days_combo.addItems(["7", "14", "30", "60", "90"])
        self.days_combo.setCurrentText(str(self.settings.get("keep_logs_days", 30)))
        self.days_combo.setFixedWidth(200)
        days_row.addWidget(days_label)
        days_row.addStretch()
        days_row.addWidget(self.days_combo)
        layout.addLayout(days_row)

        return section

    def create_actions(self):
        """Create action buttons"""
        actions_container = QFrame()
        actions_container.setObjectName("settingsActions")

        layout = QHBoxLayout(actions_container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Reset button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setObjectName("resetButton")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_settings)
        layout.addWidget(reset_btn)

        layout.addStretch()

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.cancel_changes)
        layout.addWidget(cancel_btn)

        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("saveButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_changes)
        layout.addWidget(save_btn)

        return actions_container

    def save_changes(self):
        """Save all settings changes"""
        self.settings["theme"] = self.theme_combo.currentText()
        self.settings["auto_update_check"] = self.auto_update_check.isChecked()
        self.settings["confirm_installations"] = self.confirm_install.isChecked()
        self.settings["confirm_removals"] = self.confirm_remove.isChecked()
        self.settings["auto_clean_cache"] = self.auto_clean.isChecked()
        self.settings["parallel_downloads"] = int(self.parallel_combo.currentText())
        self.settings["default_helper"] = self.helper_combo.currentText()
        self.settings["show_aur_warnings"] = self.show_warnings.isChecked()
        self.settings["log_level"] = self.level_combo.currentText()
        self.settings["keep_logs_days"] = int(self.days_combo.currentText())

        if self.save_settings():
            QMessageBox.information(self, "Settings", "Settings saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to save settings.")

    def cancel_changes(self):
        """Discard changes and reload settings"""
        self.settings = self.load_settings()
        self.theme_combo.setCurrentText(self.settings.get("theme", "Dark"))
        self.auto_update_check.setChecked(self.settings.get("auto_update_check", True))
        self.confirm_install.setChecked(self.settings.get("confirm_installations", True))
        self.confirm_remove.setChecked(self.settings.get("confirm_removals", True))
        self.auto_clean.setChecked(self.settings.get("auto_clean_cache", False))
        self.parallel_combo.setCurrentText(str(self.settings.get("parallel_downloads", 5)))
        self.helper_combo.setCurrentText(self.settings.get("default_helper", "yay"))
        self.show_warnings.setChecked(self.settings.get("show_aur_warnings", True))
        self.level_combo.setCurrentText(self.settings.get("log_level", "Info"))
        self.days_combo.setCurrentText(str(self.settings.get("keep_logs_days", 30)))

    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            self.settings = self.load_settings()
            self.cancel_changes()
            QMessageBox.information(self, "Settings", "Settings reset to defaults.")
