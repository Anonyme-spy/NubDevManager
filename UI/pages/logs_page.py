from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QTextEdit, QScrollArea)
from PyQt6.QtCore import Qt


class LogsPage(QWidget):
    """Logs page - View installation logs and system activity"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the logs page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Page title and description
        title = QLabel("System Logs")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel("View installation logs and system activity")
        desc.setObjectName("pageDescription")
        layout.addWidget(desc)

        # Control buttons
        controls = self.create_controls()
        layout.addWidget(controls)

        # Recent activity summary
        recent_activity = self.create_recent_activity()
        layout.addWidget(recent_activity)

        # Log viewer
        log_viewer = self.create_log_viewer()
        layout.addWidget(log_viewer)

    def create_controls(self):
        """Create control buttons for log management"""
        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("controlButton")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Clear logs button
        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.setObjectName("controlButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Export button
        export_btn = QPushButton("📥 Export Logs")
        export_btn.setObjectName("controlButton")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        controls_layout.addWidget(refresh_btn)
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(export_btn)
        controls_layout.addStretch()

        return controls_container

    def create_recent_activity(self):
        """Create recent activity summary cards"""
        activity_container = QWidget()
        grid = QGridLayout(activity_container)
        grid.setSpacing(15)

        # Activity data: title, count, icon, color
        activities = [
            ("Successful Installs", "8", "✓", "#10B981"),
            ("Failed Operations", "1", "✗", "#EF4444"),
            ("Updates Available", "5", "↑", "#F59E0B"),
            ("Total Actions", "24", "📊", "#3B82F6"),
        ]

        # Create activity cards
        for i, (title, count, icon, color) in enumerate(activities):
            card = self.create_activity_card(title, count, icon, color)
            grid.addWidget(card, 0, i)

        return activity_container

    def create_activity_card(self, title, count, icon, color):
        """Create an individual activity summary card"""
        card = QFrame()
        card.setObjectName("activityCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Icon with colored background
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(
            f"font-size: 24px; background-color: {color}; padding: 10px; border-radius: 6px; color: white;")
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Count
        count_label = QLabel(count)
        count_label.setObjectName("activityCount")

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("activityTitle")
        title_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(count_label)
        layout.addWidget(title_label)

        return card

    def create_log_viewer(self):
        """Create the main log viewer text area"""
        viewer_container = QFrame()
        viewer_container.setObjectName("logViewerContainer")

        layout = QVBoxLayout(viewer_container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setObjectName("logViewerHeader")
        header.setFixedHeight(50)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        header_label = QLabel("Installation Log")
        header_label.setObjectName("logViewerTitle")
        header_layout.addWidget(header_label)

        header_layout.addStretch()

        # Filter buttons
        filter_all = QPushButton("All")
        filter_all.setObjectName("logFilterActive")
        filter_error = QPushButton("Errors")
        filter_error.setObjectName("logFilter")
        filter_warning = QPushButton("Warnings")
        filter_warning.setObjectName("logFilter")
        filter_info = QPushButton("Info")
        filter_info.setObjectName("logFilter")

        header_layout.addWidget(filter_all)
        header_layout.addWidget(filter_error)
        header_layout.addWidget(filter_warning)
        header_layout.addWidget(filter_info)

        layout.addWidget(header)

        # Log text area
        log_text = QTextEdit()
        log_text.setObjectName("logTextArea")
        log_text.setReadOnly(True)

        # Sample log content
        sample_logs = """[2026-01-12 14:32:15] [INFO] Starting Dev Manager v1.0.0
[2026-01-12 14:32:16] [INFO] Checking system dependencies...
[2026-01-12 14:32:17] [SUCCESS] All system dependencies satisfied
[2026-01-12 14:33:42] [INFO] Installing package: python3.12
[2026-01-12 14:33:45] [INFO] Downloading python3.12 (25.4 MB)...
[2026-01-12 14:34:12] [SUCCESS] python3.12 installed successfully
[2026-01-12 14:35:20] [INFO] Installing package: nodejs
[2026-01-12 14:35:23] [INFO] Downloading nodejs (18.2 MB)...
[2026-01-12 14:35:48] [SUCCESS] nodejs installed successfully
[2026-01-12 14:36:15] [INFO] Installing package: docker
[2026-01-12 14:36:18] [ERROR] Failed to install docker: dependency conflict
[2026-01-12 14:36:18] [ERROR] Missing dependency: containerd.io >= 1.6.0
[2026-01-12 14:37:05] [WARNING] 5 packages have available updates
[2026-01-12 14:37:06] [INFO] Run 'sudo apt update && sudo apt upgrade' to update
[2026-01-12 14:38:22] [INFO] Installing package: git
[2026-01-12 14:38:24] [INFO] Downloading git (12.8 MB)...
[2026-01-12 14:38:39] [SUCCESS] git installed successfully
[2026-01-12 14:39:15] [INFO] Cleaning up temporary files...
[2026-01-12 14:39:16] [SUCCESS] Cleanup completed
[2026-01-12 14:39:16] [INFO] Dev Manager ready"""

        log_text.setPlainText(sample_logs)

        layout.addWidget(log_text)

        return viewer_container