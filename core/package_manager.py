import subprocess
import shutil
import platform

class PackageManager:
    def __init__(self):
        self.manager = self._detect_package_manager()
        self.distro = self._detect_distro()

    # linux_distribution detection
    def _detect_distro(self):
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                info = {}
                for line in lines:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        info[key] = value.strip('"')
                return {
                    "id": info.get("ID", "unknown"),
                    "name": info.get("NAME", "Unknown"),
                    "version": info.get("VERSION_ID", ""),
                    "id_like": info.get("ID_LIKE", "").split(),
                }
        except FileNotFoundError:
            return {"id": "unknown", "name": "Unknown", "version": "", "id_like": []}

    # package manager detection
    def _detect_package_manager(self):
        if shutil.which('apt'):
            return 'apt'
        elif shutil.which('yum'):
            return 'yum'
        elif shutil.which('dnf'):
            return 'dnf'
        elif shutil.which('pacman'):
            return 'pacman'
        elif shutil.which('apt-get'):
            return 'apt'
        elif shutil.which('zypper'):
            return 'zypper'
        else:
            raise EnvironmentError("No supported package manager found.")

    # privilege check
    def _get_privilege_command(self):
        if shutil.which("pkexec"):
            return ["pkexec"]
        elif shutil.which("gksudo"):
            return ["gksudo", "--"]
        elif shutil.which("kdesudo"):
            return ["kdesudo", "--"]
        elif shutil.which("sudo"):
            return ["sudo"]
        else:
            raise EnvironmentError("No privilege escalation method found.")

    # install a package
    def install(self, package: str) -> bool:
        commands = {
            "apt": ["apt", "install", "-y", package],
            "yum": ["yum", "install", "-y", package],
            "dnf": ["dnf", "install", "-y", package],
            "pacman": ["pacman", "-S", "--noconfirm", package],
            "zypper": ["zypper", "install", "-y", package],
        }
        if self.manager:
            try:
                full_cmd = self._get_privilege_command() + commands[self.manager]
                subprocess.run(full_cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    # update package lists
    def update(self) -> bool:
        commands = {
            "apt": ["apt", "update"],
            "yum": ["yum", "check-update"],
            "dnf": ["dnf", "check-update"],
            "pacman": ["pacman", "-Sy"],
            "zypper": ["zypper", "refresh"],
        }
        if self.manager:
            try:
                full_cmd = self._get_privilege_command() + commands[self.manager]
                subprocess.run(full_cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    # check if a package is installed
    def is_installed(self, package: str) -> bool:
        commands = {
            "apt": ["dpkg", "-s", package],
            "yum": ["rpm", "-q", package],
            "dnf": ["rpm", "-q", package],
            "pacman": ["pacman", "-Qi", package],
            "zypper": ["rpm", "-q", package],
        }
        try:
            subprocess.run(commands[self.manager], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    # update a specific package
    def upgrade(self, package: str) -> bool:
        commands = {
            "apt": ["apt", "install", "--only-upgrade", "-y", package],
            "yum": ["yum", "update", "-y", package],
            "dnf": ["dnf", "upgrade", "-y", package],
            "pacman": ["pacman", "-S", "--noconfirm", package],
            "zypper": ["zypper", "update", "-y", package],
        }
        if self.manager:
            try:
                full_cmd = self._get_privilege_command() + commands[self.manager]
                subprocess.run(full_cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    # remove a package
    def remove(self, package: str) -> bool:
        commands = {
            "apt": ["apt", "remove", "-y", package],
            "yum": ["yum", "remove", "-y", package],
            "dnf": ["dnf", "remove", "-y", package],
            "pacman": ["pacman", "-R", "--noconfirm", package],
            "zypper": ["zypper", "remove", "-y", package],
        }
        if self.manager:
            try:
                full_cmd = self._get_privilege_command() + commands[self.manager]
                subprocess.run(full_cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def cleanup(self, package: str) -> bool:
        commands = {
            "apt": ["apt", "autoremove", "-y", package],
            "yum": ["yum", "autoremove", "-y", package],
            "dnf": ["dnf", "autoremove", "-y", package],
            "pacman": ["pacman", "-Rns", "--noconfirm", package],
            "zypper": ["zypper", "autoremove", "-y", package],
        }
        if self.manager:
            try:
                full_cmd = self._get_privilege_command() + commands[self.manager]
                subprocess.run(full_cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False














