# WUI - Wine User Interface

WUI (Wine User Interface) is a modern Linux desktop application that simplifies running Windows executables (.exe) using Wine.

## Prerequisites

- **Python 3**: Ensure Python 3 is installed.
- **Wine**: The application requires Wine to be installed on your system.
    ```bash
    sudo apt install wine
    ```

## Installation

1.  **Install Python Pip** (if not already installed):
    ```bash
    sudo apt install python3-pip
    ```

2.  **Install Dependencies**:
    Navigate to the project directory and install the required Python packages:
    ```bash
    pip3 install -r requirements.txt
    ```
    *Note: On some systems, you might need to use `python3 -m pip install -r requirements.txt` or install into a virtual environment.*
    
    If you prefer using system packages for Qt (recommended on some Linux distros):
    ```bash
    sudo apt install python3-pyside6
    ```

## Usage

1.  Run the application:
    ```bash
    python3 main.py
    ```

2.  **Select Executable**: Click "Browse" to find the Windows executable (`.exe`) you want to run.
3.  **Launch**: Click the "Launch Application" button.
