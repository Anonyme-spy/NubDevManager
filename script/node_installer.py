from core.package_manager import PackageManager

class NodeInstaller:
    def __init__(self):
        self.pkg_manager = PackageManager()

    def install(self):
        return self.pkg_manager.install("nodejs")

    def is_installed(self):
        return self.pkg_manager.is_installed("nodejs")

    def update(self):
        return self.pkg_manager.upgrade("nodejs")

    def remove(self):
        return self.pkg_manager.remove("nodejs")
