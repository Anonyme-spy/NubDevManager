# core/aur_manager.py
import subprocess
import shutil
import os
import tempfile


class AURManager:
    """Manages AUR helpers (yay, paru, etc.) and AUR package operations"""

    SUPPORTED_HELPERS = {
        "yay": {
            "name": "yay",
            "description": "Yet Another Yogurt - An AUR Helper written in Go",
            "git_url": "https://aur.archlinux.org/yay.git",
            "deps": ["git", "base-devel"]
        },
        "paru": {
            "name": "paru",
            "description": "Feature packed AUR helper written in Rust",
            "git_url": "https://aur.archlinux.org/paru.git",
            "deps": ["git", "base-devel", "rust"]
        },
        "trizen": {
            "name": "trizen",
            "description": "Lightweight AUR Package Manager written in Perl",
            "git_url": "https://aur.archlinux.org/trizen.git",
            "deps": ["git", "base-devel", "perl"]
        }
    }

    def __init__(self):
        self.active_helper = self._detect_aur_helper()
        self.is_arch_based = self._check_arch_based()

    def _check_arch_based(self) -> bool:
        """Check if the system is Arch-based"""
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                return "arch" in content or shutil.which("pacman") is not None
        except FileNotFoundError:
            return shutil.which("pacman") is not None

    def _detect_aur_helper(self) -> str | None:
        """Detect installed AUR helper"""
        for helper in ["yay", "paru", "trizen"]:
            if shutil.which(helper):
                return helper
        return None

    def is_helper_installed(self, helper_name: str) -> bool:
        """Check if a specific AUR helper is installed"""
        return shutil.which(helper_name) is not None

    def get_installed_helpers(self) -> list[str]:
        """Get list of installed AUR helpers"""
        return [h for h in self.SUPPORTED_HELPERS.keys() if self.is_helper_installed(h)]

    def install_helper(self, helper_name: str) -> tuple[bool, str]:
        """Install an AUR helper from source"""
        if helper_name not in self.SUPPORTED_HELPERS:
            return False, f"Unknown AUR helper: {helper_name}"

        if not self.is_arch_based:
            return False, "AUR helpers are only available on Arch-based systems"

        helper_info = self.SUPPORTED_HELPERS[helper_name]

        try:
            # Install dependencies first
            for dep in helper_info["deps"]:
                subprocess.run(
                    ["sudo", "pacman", "-S", "--noconfirm", "--needed", dep],
                    check=True,
                    capture_output=True
                )

            # Clone and build in temp directory
            with tempfile.TemporaryDirectory() as tmpdir:
                # Clone the repository
                subprocess.run(
                    ["git", "clone", helper_info["git_url"]],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True
                )

                build_dir = os.path.join(tmpdir, helper_name)

                # Build and install
                subprocess.run(
                    ["makepkg", "-si", "--noconfirm"],
                    cwd=build_dir,
                    check=True
                )

            # Update active helper
            self.active_helper = self._detect_aur_helper()
            return True, f"Successfully installed {helper_name}"

        except subprocess.CalledProcessError as e:
            return False, f"Failed to install {helper_name}: {e}"
        except Exception as e:
            return False, f"Error installing {helper_name}: {str(e)}"

    def remove_helper(self, helper_name: str) -> tuple[bool, str]:
        """Remove an AUR helper"""
        if not self.is_helper_installed(helper_name):
            return False, f"{helper_name} is not installed"

        try:
            subprocess.run(
                ["sudo", "pacman", "-Rns", "--noconfirm", helper_name],
                check=True,
                capture_output=True
            )
            self.active_helper = self._detect_aur_helper()
            return True, f"Successfully removed {helper_name}"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to remove {helper_name}: {e}"

    def search_aur(self, query: str) -> list[dict]:
        """Search AUR packages"""
        if not self.active_helper:
            return []

        try:
            result = subprocess.run(
                [self.active_helper, "-Ss", query],
                capture_output=True,
                text=True,
                timeout=30
            )

            packages = []
            lines = result.stdout.strip().split('\n')
            i = 0
            while i < len(lines):
                if lines[i].startswith('aur/'):
                    parts = lines[i].split()
                    if len(parts) >= 2:
                        name_part = parts[0].replace('aur/', '')
                        version = parts[1] if len(parts) > 1 else "unknown"

                        # Get description from next line if available
                        description = ""
                        if i + 1 < len(lines) and not lines[i + 1].startswith('aur/'):
                            description = lines[i + 1].strip()
                            i += 1

                        # Extract votes and popularity if present
                        votes = "0"
                        popularity = "0"
                        for part in parts:
                            if part.startswith('(+'):
                                votes = part.strip('()+')
                            elif part.endswith('%'):
                                popularity = part.strip('%')

                        packages.append({
                            "name": name_part,
                            "version": version,
                            "description": description,
                            "votes": votes,
                            "popularity": popularity
                        })
                i += 1

            return packages

        except subprocess.TimeoutExpired:
            return []
        except Exception:
            return []

    def install_package(self, package_name: str) -> tuple[bool, str]:
        """Install a package from AUR"""
        if not self.active_helper:
            return False, "No AUR helper installed"

        try:
            subprocess.run(
                [self.active_helper, "-S", "--noconfirm", package_name],
                check=True
            )
            return True, f"Successfully installed {package_name}"
        except subprocess.CalledProcessError:
            return False, f"Failed to install {package_name}"

    def remove_package(self, package_name: str) -> tuple[bool, str]:
        """Remove an AUR package"""
        if not self.active_helper:
            return False, "No AUR helper installed"

        try:
            subprocess.run(
                [self.active_helper, "-Rns", "--noconfirm", package_name],
                check=True
            )
            return True, f"Successfully removed {package_name}"
        except subprocess.CalledProcessError:
            return False, f"Failed to remove {package_name}"

    def is_package_installed(self, package_name: str) -> bool:
        """Check if a package is installed"""
        try:
            subprocess.run(
                ["pacman", "-Qi", package_name],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def get_installed_aur_packages(self) -> list[dict]:
        """Get list of installed foreign (AUR) packages"""
        try:
            result = subprocess.run(
                ["pacman", "-Qm"],
                capture_output=True,
                text=True
            )

            packages = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append({
                            "name": parts[0],
                            "version": parts[1]
                        })
            return packages
        except Exception:
            return []
