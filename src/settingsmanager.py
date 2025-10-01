# TODO: Change to JSON
# Make async since its accessing IO(disk)
import json
from typing import Any, Optional, Callable
import pathlib
import os
CONFIG_PATH = pathlib.Path(__file__).parent / "config.json"

async def ensure_config():
    try:
        with open(CONFIG_PATH, "r"):
            print(f"\033[32mINFO\033[0m:     Settings Manager Up! Path: {CONFIG_PATH}")
    except FileNotFoundError:
        print("\033[32mWARN\033[0m:     Settings file not found! Creating...")
        with open(CONFIG_PATH, "x"):
            print(f"\033[1;33mINFO\033[0m:     File created! Path: {CONFIG_PATH}")

def read_config():
    """
    Reads and parses a JSON configuration file.
    Returns an empty dictionary if the file is not found or is empty.
    """
    try:
        if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        else:
            return {}  # Return an empty dict if the file is empty or doesn't exist
    except json.JSONDecodeError:
        print("\033[31mError\033[0m:     Invalid JSON format in config file.")
        return {}


def write_config(content: dict) -> bool:
    """
    Reads a JSON config file, updates it with new content, and writes it back.
    """
    try:
        # Open the file for reading and load the data.
        # Handles empty file by starting with an empty dict.
        if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
        else:
            data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid JSON, start with a fresh dict.
        data = {}

    # Update the dictionary with the new content.
    data.update(content)

    # Open the file in write mode ('w') to overwrite it with the updated data.
    with open(CONFIG_PATH, "w") as f:
        # Use json.dump() to write the Python object to the file.
        json.dump(data, f, indent=4)
        
    return True