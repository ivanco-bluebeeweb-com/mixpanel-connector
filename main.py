"""Entry point for Mixpanel Connector."""
import os, sys
_EXT_DIR = os.path.dirname(os.path.abspath(__file__))
if _EXT_DIR not in sys.path:
    sys.path.insert(0, _EXT_DIR)

for _mod in ("app", "schemas", "mixpanel_connector_client", "handlers_connection", "handlers_resources", "panels"):
    sys.modules.pop(_mod, None)

from app import ext, chat
app = ext
import handlers_connection  # noqa: E402,F401
import handlers_resources   # noqa: E402,F401
import panels               # noqa: E402,F401

__all__ = ["app", "chat"]
