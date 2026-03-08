import importlib.util
from pathlib import Path


class PluginLoader:

    def __init__(self, plugin_folder="plugins"):

        self.plugin_folder = Path(plugin_folder)
        self.plugins = []

        self.load_plugins()

    # ================================
    # LOAD ALL PLUGINS
    # ================================

    def load_plugins(self):

        if not self.plugin_folder.exists():
            print("Plugin folder not found.")
            return

        for file in self.plugin_folder.glob("*.py"):

            try:
                spec = importlib.util.spec_from_file_location(
                    file.stem,
                    file
                )

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "Plugin"):
                    plugin_instance = module.Plugin()
                    self.plugins.append(plugin_instance)
                    print(f"Loaded plugin: {file.stem}")

            except Exception as e:
                print(f"Plugin load error ({file.name}):", e)

    # ================================
    # HANDLE COMMAND
    # ================================

    def handle(self, command: str):

        for plugin in self.plugins:
            try:
                if plugin.match(command):
                    return plugin.run(command)
            except Exception as e:
                print("Plugin execution error:", e)

        return None