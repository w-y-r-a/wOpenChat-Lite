from configparser import ConfigParser
from typing import Any, Optional, Callable
import pathlib
CONFIG_PATH = pathlib.Path(__file__).parent / "config.ini"
config = ConfigParser()
config.read(CONFIG_PATH)

def _ensure_loaded() -> None:
    # Read once; ConfigParser.read is idempotent and cheap
    if not getattr(_ensure_loaded, "_loaded", False):
        config.read(CONFIG_PATH)
        setattr(_ensure_loaded, "_loaded", True)

def init_config() -> None:
    """
    Ensure config is loaded and required sections exist.
    Call this during startup before DB init.
    """
    _ensure_loaded()
    # Ensure sections exist
    for section in ("Customization", "Global", "Database"):
        if not config.has_section(section):
            config.add_section(section)
    # Optionally set safe defaults
    if not config.has_option("Global", "setup_complete"):
        config.set("Global", "setup_complete", "false")

def _convert(value: str, caster: Optional[Callable[[str], Any]]) -> Any:
    if caster is None:
        return value
    try:
        return caster(value)
    except Exception:
        return None

def read_config(section: str, key: str, *, cast: Optional[Callable[[str], Any]] = None) -> Optional[Any]:
    """
    Returns None if section/key missing. Optionally cast the string value.
    """
    _ensure_loaded()
    if config.has_option(section, key):
        return _convert(config.get(section, key), cast)
    return None

def write_config(section: str, key: str, new: Any) -> None:
    """
    Writes value as string and persists to disk. Ensures section exists.
    """
    _ensure_loaded()
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, str(new))
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)

if __name__ != "__main__":
    print(f"\033[32mINFO\033[0m:     Settings Manager Up! Path: {CONFIG_PATH}")