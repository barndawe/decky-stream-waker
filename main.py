import os
import sys
import logging
from pathlib import Path
import decky_plugin

DEPSPATH = Path(decky_plugin.DECKY_PLUGIN_DIR) / "backend/out"


std_out_file = open(Path(decky_plugin.DECKY_PLUGIN_LOG_DIR) / "decky-stream-waker-std-out.log", "w")
std_err_file = open(Path(decky_plugin.DECKY_PLUGIN_LOG_DIR) / "decky-stream-waker-std-err.log", "w")

logger = decky_plugin.logger

from logging.handlers import TimedRotatingFileHandler
log_file = Path(decky_plugin.DECKY_PLUGIN_LOG_DIR) / "decky-stream-waker.log"
log_file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=2)
log_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.handlers.clear()
logger.addHandler(log_file_handler)

try:
    sys.path.append(str(DEPSPATH / "wakeonlan"))
    from wakeonlan import send_magic_packet

    logger.info("Successfully loaded wakeonlan")
except Exception:
    logger.info(traceback.format_exc())

class Plugin:
    async def wake(self):
        send_magic_packet(os.environ.get("PC_MAC"))

    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)
    async def add(self, left, right):
        return left + right

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        decky_plugin.logger.info("Hello World!")

    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        decky_plugin.logger.info("Goodbye World!")
        pass

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky_plugin.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be migrated to `decky_plugin.DECKY_PLUGIN_LOG_DIR/template.log`
        decky_plugin.migrate_logs(os.path.join(decky_plugin.DECKY_USER_HOME,
                                               ".config", "decky-template", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky_plugin.DECKY_PLUGIN_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_SETTINGS_DIR/`
        decky_plugin.migrate_settings(
            os.path.join(decky_plugin.DECKY_HOME, "settings", "template.json"),
            os.path.join(decky_plugin.DECKY_USER_HOME, ".config", "decky-template"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_RUNTIME_DIR/`
        decky_plugin.migrate_runtime(
            os.path.join(decky_plugin.DECKY_HOME, "template"),
            os.path.join(decky_plugin.DECKY_USER_HOME, ".local", "share", "decky-template"))
