from src.settingsmanager import read_config


def get_customization_config() -> dict:
    """
    Retrieves customization configuration values (theme_color, favicon_url, setup_complete).
    Returns None for values that cannot be retrieved.
    
    Returns:
        dict: A dictionary containing theme_color, favicon_url, and setup_complete
    """
    config = {}
    
    try:
        config["theme_color"] = read_config().get("customization").get("theme_color")  # pyright: ignore[reportOptionalMemberAccess]
    except (AttributeError, KeyError, TypeError):
        config["theme_color"] = None
    
    try:
        config["favicon_url"] = read_config().get("customization").get("favicon_url")  # pyright: ignore[reportOptionalMemberAccess]
    except (AttributeError, KeyError, TypeError):
        config["favicon_url"] = None
    
    try:
        config["setup_complete"] = read_config().get("global").get("setup_complete")  # pyright: ignore[reportOptionalMemberAccess]
    except (AttributeError, KeyError, TypeError):
        config["setup_complete"] = False
    
    return config
