from configparser import ConfigParser
import pathlib
from typing import Optional

# Global configuration storage
config = {}

def init_config() -> None:
    """
    Initialize the global config dict. Call this at startup before any read_config/write_config.
    """
    global config
    # Load from disk/env/defaults as needed.
    # Example placeholder: ensure required sections exist.
    if not isinstance(config, dict):
        config = {}
    config.setdefault("Customization", {})
    config.setdefault("Global", {})
    config.setdefault("Database", {})

def read_config(section: str, key: str) -> Optional[str]:
    """
    Safe read from the global config. Returns None if not set or config not initialized.
    """
    try:
        return config[section][key]
    except Exception:
        return None

def write_config(section: str, key: str, value: str) -> None:
    """
    Safe write into the global config.
    """
    global config
    if not isinstance(config, dict):
        config = {}
    if section not in config or not isinstance(config[section], dict):
        config[section] = {}
    config[section][key] = value