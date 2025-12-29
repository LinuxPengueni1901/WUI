#!/usr/bin/env python3
import sys
import subprocess
import shutil
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont, QColor, QPalette

class ModernButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(45)
        
        # Base style
        base_style = """
            QPushButton {
                border-radius: 8px;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-weight: 600;
                font-size: 14px;
                padding: 0 20px;
            }
        """
        
        if primary:
            self.setStyleSheet(base_style + """
                QPushButton {
                    background-color: #7c4dff;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #651fff;
                }
                QPushButton:pressed {
                    background-color: #6200ea;
                }
            """)
        else:
            self.setStyleSheet(base_style + """
                QPushButton {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border: 1px solid #505050;
                }
                QPushButton:pressed {
                    background-color: #252525;
                }
            """)

class WUIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WUI - Wine User Interface")
        self.setMinimumSize(600, 400)
        
        # Setup dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                padding: 10px;
                font-size: 13px;
                selection-background-color: #7c4dff;
            }
            QLineEdit:focus {
                border: 1px solid #7c4dff;
            }
        """)

        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Wine Runner")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        subtitle_label = QLabel("Select a Windows executable (.exe) to run seamlessly on Linux")
        subtitle_label.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addLayout(header_layout)

        # Content Area
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 12px;
                border: 1px solid #333333;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # File Selection Block
        file_label = QLabel("Executable Path")
        file_label.setStyleSheet("font-weight: 600; color: #cccccc;")
        content_layout.addWidget(file_label)

        input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select .exe file...")
        input_layout.addWidget(self.path_input)

        browse_btn = ModernButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setFixedWidth(100)
        input_layout.addWidget(browse_btn)
        
        content_layout.addLayout(input_layout)
        
        # Status/Preview
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666666; font-size: 12px; font-style: italic;")
        content_layout.addWidget(self.status_label)

        layout.addWidget(content_frame)

        # Actions
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.run_btn = ModernButton("Launch Application", primary=True)
        self.run_btn.clicked.connect(self.run_application)
        self.run_btn.setMinimumWidth(150)
        action_layout.addWidget(self.run_btn)
        
        layout.addLayout(action_layout)
        layout.addStretch()

        # Check for wine
        self.check_wine_installation()

    def check_wine_installation(self):
        # If in Flatpak, we assume host might have wine, 
        # checking host wine from sandbox is tricky without executing.
        if os.path.exists("/.flatpak-info"):
            return

        if not shutil.which("wine"):
            QMessageBox.warning(self, "Wine Not Found", 
                              "Wine is not detected in your system path.\n"
                              "Please make sure Wine is installed to use this application.")
            self.status_label.setText("Error: Wine not found")
            self.status_label.setStyleSheet("color: #ff5252;")
            self.run_btn.setEnabled(False)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Windows Executable",
            os.path.expanduser("~"),
            "Executables (*.exe);;All Files (*)"
        )
        if file_name:
            self.path_input.setText(file_name)
            self.status_label.setText(f"Ready to launch: {os.path.basename(file_name)}")
            self.status_label.setStyleSheet("color: #4caf50;")

    def run_application(self):
        exe_path = self.path_input.text().strip()
        if not exe_path:
            QMessageBox.warning(self, "No File Selected", "Please select an executable file first.")
            return

        if not os.path.exists(exe_path):
            QMessageBox.critical(self, "File Not Found", "The specified file does not exist.")
            return

        try:
            # Check if running in Flatpak
            is_flatpak = os.path.exists("/.flatpak-info")
            
            cmd = []
            if is_flatpak:
                # Use flatpak-spawn to run on host
                cmd = ["flatpak-spawn", "--host", "wine", exe_path]
            else:
                cmd = ["wine", exe_path]

            # Using Popen to run detached
            subprocess.Popen(cmd, 
                           cwd=os.path.dirname(exe_path),
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            
            self.status_label.setText(f"Running: {os.path.basename(exe_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"Failed to run application:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set app style
    app.setStyle("Fusion")
    
    # Set App ID for desktop file association
    app.setDesktopFileName("io.github.linuxpengueni1901.WUI")
    
    # Set Application Icon (Global)
    # 1. Try local assets (for development)
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    
    # 2. Try standard installation path (for Flatpak/Linux install)
    if not os.path.exists(icon_path):
        icon_path = "/app/share/icons/hicolor/512x512/apps/io.github.linuxpengueni1901.WUI.png"

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Warning: Icon not found")

    window = WUIApp()
    window.show()
    
    sys.exit(app.exec())
