# Dev Manager

A Linux development tools manager built with PyQt6. This desktop application provides a user-friendly interface for installing and managing development tools on Linux systems.

## ⚠️ Disclaimer

**This project is for learning purposes only.** It was created as a practice project to learn:
- PyQt6 GUI development
- Linux package management systems
- Python application architecture
- CSS styling for desktop applications

AI tools (GitHub Copilot) were used to assist with UI design and styling decisions.

## Features

- **Individual Tools** - Browse and install development tools one by one
- **Dev Packs** - Install curated bundles of tools for specific workflows
- **AUR Installer** - Search and install packages from the Arch User Repository
- **Logs** - View installation logs and system activity
- **Settings** - Configure application preferences

## Supported Package Managers

- `apt` (Debian/Ubuntu)
- `dnf` (Fedora)
- `yum` (RHEL/CentOS)
- `pacman` (Arch Linux)
- `zypper` (openSUSE)

## Requirements

- Python 3.10+
- PyQt6
- Linux operating system

## Installation

```bash
git clone https://github.com/Anonyme-spy/dev-manager.git
cd dev-manager
pip install PyQt6
python main.py
```
```
dev-manager/
├── main.py                 # Entry point
├── core/
│   └── package_manager.py  # Package management logic
├── assets/
├── script/
│   └── node_installer.py  # installer scripts
└── UI/
    ├── app.py              # Main application window
    ├── style.css           # Application styling
    └── pages/
        ├── __init__.py
        ├── home_page.py
        ├── individual_tools_page.py
        ├── dev_packs_page.py
        ├── aur_installer_page.py
        ├── logs_page.py
        └── settings_page.py

License
This project is for educational purposes only.
```