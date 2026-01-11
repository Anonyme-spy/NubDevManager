from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QCheckBox, QComboBox,
                             QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt


class SettingsPage(QWidget):
    """Settings page - Configure Dev Manager preferences and options"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the settings page UI"""
        # Main scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Page title and description
        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel("Configure Dev Manager preferences and options")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # General settings section
        general_section = self.create_settings_section(
            "General",
            [
                ("Auto-update package lists", "checkbox", True),
                ("Show notifications", "checkbox", True),
                ("Confirm before installing", "checkbox", True),
                ("Theme", "combo", ["Dark", "Light", "System"])
            ]
        )
        layout.addWidget(general_section)

        # Installation settings section
        install_section = self.create_settings_section(
            "Installation",
            [
                ("Parallel downloads", "checkbox", True),
                ("Max download threads", "combo", ["2", "4", "8", "16"]),
                ("Keep downloaded packages", "checkbox", False),
                ("Verify package signatures", "checkbox", True)
            ]
        )
        layout.addWidget(install_section)

        # AUR settings section
        aur_section = self.create_settings_section(
            "AUR Configuration",
            [
                ("Enable AUR support", "checkbox", True),
                ("Build directory", "text", "/tmp/aur-builds"),
                ("Clean build directory", "checkbox", True),
                ("AUR helper", "combo", ["yay", "paru", "pikaur"])
            ]
        )
        layout.addWidget(aur_section)

        # System settings section
        system_section = self.create_settings_section(
            "System",
            [
                ("Log level", "combo", ["INFO", "DEBUG", "WARNING", "ERROR"]),
                ("Log retention (days)", "combo", ["7", "14", "30", "90"]),
                ("Enable system monitoring", "checkbox", True),
                ("Auto-cleanup old logs", "checkbox", True)
            ]
        )
        layout.addWidget(system_section)

        # Action buttons at bottom
        actions = self.create_action_buttons()
        layout.addWidget(actions)

        layout.addStretch()

        scroll.setWidget(scroll_content)

        # Set scroll area as main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def create_settings_section(self, section_title, settings_items):
        """
        Create a settings section with multiple options

        Args:
            section_title: Title of the settings section
            settings_items: List of tuples (label, type, default_value)
                           type can be: "checkbox", "combo", or "text"
        """
        section = QFrame()
        section.setObjectName("settingsSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Section title
        title = QLabel(section_title)
        title.setObjectName("settingsSectionTitle")
        layout.addWidget(title)

        # Add settings items
        for label_text, item_type, default_value in settings_items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(15)

            # Label
            label = QLabel(label_text)
            label.setObjectName("settingsLabel")
            item_layout.addWidget(label)

            item_layout.addStretch()

            # Control based on type
            if item_type == "checkbox":
                control = QCheckBox()
                control.setObjectName("settingsCheckbox")
                control.setChecked(default_value)
                control.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(control)

            elif item_type == "combo":
                control = QComboBox()
                control.setObjectName("settingsCombo")
                control.addItems(default_value if isinstance(default_value, list) else [default_value])
                control.setFixedWidth(200)
                control.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(control)

            elif item_type == "text":
                control = QLineEdit(default_value)
                control.setObjectName("settingsInput")
                control.setFixedWidth(300)
                item_layout.addWidget(control)

            layout.addLayout(item_layout)

        return section

    def create_action_buttons(self):
        """Create action buttons for settings page"""
        actions_container = QFrame()
        actions_container.setObjectName("settingsActions")

        layout = QHBoxLayout(actions_container)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        # Reset to defaults button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setObjectName("resetButton")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(reset_btn)
        layout.addStretch()

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.setFixedWidth(100)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("saveButton")
        save_btn.setFixedWidth(120)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)

        return actions_container