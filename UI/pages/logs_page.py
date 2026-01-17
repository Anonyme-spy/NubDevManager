# UI/pages/logs_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QTextEdit, QScrollArea,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QTextCursor
import os


class LogsPage(QWidget):
    """Logs page - View installation and operation logs"""

    def __init__(self):
        super().__init__()
        self.current_filter = "All"
        self.log_entries = []
        self.init_ui()
        self.load_sample_logs()

    def init_ui(self):
        """Initialize the logs page UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        # Page title and description
        title = QLabel("Logs")
        title.setObjectName("pageTitle")
        self.main_layout.addWidget(title)

        desc = QLabel("View installation logs and system activity")
        desc.setObjectName("pageDescription")
        self.main_layout.addWidget(desc)

        # Control buttons row
        controls = self.create_controls()
        self.main_layout.addWidget(controls)

        # Activity stats cards
        stats = self.create_activity_stats()
        self.main_layout.addWidget(stats)

        # Log viewer
        log_viewer = self.create_log_viewer()
        self.main_layout.addWidget(log_viewer)

    def create_controls(self):
        """Create control buttons row"""
        controls = QWidget()
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("controlButton")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_logs)
        layout.addWidget(refresh_btn)

        # Clear button
        clear_btn = QPushButton("🗑 Clear Logs")
        clear_btn.setObjectName("controlButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_logs)
        layout.addWidget(clear_btn)

        # Export button
        export_btn = QPushButton("📤 Export")
        export_btn.setObjectName("controlButton")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self.export_logs)
        layout.addWidget(export_btn)

        layout.addStretch()

        return controls

    def create_activity_stats(self):
        """Create activity statistics cards"""
        stats_container = QWidget()
        layout = QHBoxLayout(stats_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Stats data
        stats_data = [
            ("Total Operations", self.count_logs("All"), "#2563EB"),
            ("Installations", self.count_logs("Install"), "#10B981"),
            ("Removals", self.count_logs("Remove"), "#EF4444"),
            ("Updates", self.count_logs("Update"), "#F59E0B"),
        ]

        for title, count, color in stats_data:
            card = self.create_stat_card(title, count, color)
            layout.addWidget(card)

        layout.addStretch()
        return stats_container

    def create_stat_card(self, title, count, color):
        """Create a single stat card"""
        card = QFrame()
        card.setObjectName("activityCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        count_label = QLabel(str(count))
        count_label.setObjectName("activityCount")
        count_label.setStyleSheet(f"color: {color};")

        title_label = QLabel(title)
        title_label.setObjectName("activityTitle")

        layout.addWidget(count_label)
        layout.addWidget(title_label)

        return card

    def create_log_viewer(self):
        """Create the log viewer container"""
        viewer_container = QFrame()
        viewer_container.setObjectName("logViewerContainer")

        layout = QVBoxLayout(viewer_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with title and filters
        header = QFrame()
        header.setObjectName("logViewerHeader")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title = QLabel("📋 Activity Log")
        title.setObjectName("logViewerTitle")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Filter buttons
        filters = ["All", "Install", "Remove", "Update", "Error"]
        self.filter_buttons = {}

        for f in filters:
            btn = QPushButton(f)
            if f == "All":
                btn.setObjectName("logFilterActive")
            else:
                btn.setObjectName("logFilter")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, flt=f: self.on_filter_clicked(flt))
            self.filter_buttons[f] = btn
            header_layout.addWidget(btn)

        layout.addWidget(header)

        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setObjectName("logTextArea")
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        return viewer_container

    def on_filter_clicked(self, filter_name):
        """Handle filter button click"""
        self.current_filter = filter_name

        # Update button styles
        for f, btn in self.filter_buttons.items():
            if f == filter_name:
                btn.setObjectName("logFilterActive")
            else:
                btn.setObjectName("logFilter")
            btn.setStyle(btn.style())

        self.display_logs()

    def count_logs(self, log_type):
        """Count logs of a specific type"""
        if log_type == "All":
            return len(self.log_entries)
        return sum(1 for entry in self.log_entries if entry.get("type") == log_type)

    def load_sample_logs(self):
        """Load sample log entries"""
        self.log_entries = [
            {"timestamp": "2025-01-15 10:30:45", "type": "Install", "message": "Installed python3 successfully"},
            {"timestamp": "2025-01-15 10:28:12", "type": "Install", "message": "Installed nodejs successfully"},
            {"timestamp": "2025-01-15 09:45:00", "type": "Update", "message": "Updated git to version 2.43.0"},
            {"timestamp": "2025-01-14 16:20:33", "type": "Remove", "message": "Removed vim"},
            {"timestamp": "2025-01-14 14:15:22", "type": "Error", "message": "Failed to install docker: permission denied"},
            {"timestamp": "2025-01-14 11:00:00", "type": "Install", "message": "Installed docker successfully"},
        ]
        self.display_logs()

    def display_logs(self):
        """Display logs in the text area"""
        self.log_text.clear()

        filtered = self.log_entries if self.current_filter == "All" else [
            e for e in self.log_entries if e.get("type") == self.current_filter
        ]

        for entry in filtered:
            timestamp = entry.get("timestamp", "")
            log_type = entry.get("type", "Info")
            message = entry.get("message", "")

            color = {"Install": "#10B981", "Remove": "#EF4444", "Update": "#F59E0B", "Error": "#EF4444"}.get(log_type, "#8B92A8")

            self.log_text.append(f'<span style="color: #6B7280;">[{timestamp}]</span> '
                                 f'<span style="color: {color};">[{log_type}]</span> {message}')

    def add_log(self, log_type, message):
        """Add a new log entry"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.log_entries.insert(0, {"timestamp": timestamp, "type": log_type, "message": message})
        self.display_logs()

    def refresh_logs(self):
        """Refresh the logs display"""
        self.display_logs()
        self.update_stats()

    def update_stats(self):
        """Update statistics cards"""
        # Rebuild stats section
        stats_widget = self.main_layout.itemAt(3).widget()
        if stats_widget:
            self.main_layout.removeWidget(stats_widget)
            stats_widget.deleteLater()

        stats = self.create_activity_stats()
        self.main_layout.insertWidget(3, stats)

    def clear_logs(self):
        """Clear all logs"""
        reply = QMessageBox.question(
            self, "Clear Logs",
            "Are you sure you want to clear all logs?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.log_entries.clear()
            self.display_logs()
            self.update_stats()

    def export_logs(self):
        """Export logs to a file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "dev_manager_logs.txt", "Text Files (*.txt)"
        )
        if filename:
            with open(filename, 'w') as f:
                for entry in self.log_entries:
                    f.write(f"[{entry['timestamp']}] [{entry['type']}] {entry['message']}\n")
            QMessageBox.information(self, "Export", f"Logs exported to {filename}")
