# Make async since its accessing IO(disk)
import json
import pathlib
import os
import anyio
CONFIG_PATH = pathlib.Path(__file__).parent / "config.json"
_config_lock = anyio.Lock()

async def ensure_config():
    try:
        async with await anyio.open_file(CONFIG_PATH, "r"):
            print(f"\033[32mINFO\033[0m:     Settings Manager Up! Path: {CONFIG_PATH}")
    except FileNotFoundError:
        print("\033[33mWARN\033[0m:     Settings file not found! Creating...")
        async with await anyio.open_file(CONFIG_PATH, "x"):
            print(f"\033[32mINFO\033[0m:     File created! Path: {CONFIG_PATH}")

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
        print("\033[31mERROR\033[0m:     Invalid JSON format in config file.")
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

    tmp_path = CONFIG_PATH.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp_path, CONFIG_PATH)
    return True

async def async_write_config(content: dict) -> bool:
    """
    Thread- and task-safe async config writer.
    Reads, merges, and atomically writes updates.
    Prevents race conditions with an async lock.
    Args:
        content (Dict): The content to insert into the configuration file
    Returns:
        bool: If the task failed or was successful
    """
    async with _config_lock:
        data = {}

        try:
            if CONFIG_PATH.exists() and CONFIG_PATH.stat().st_size > 0:
                async with (await anyio.open_file(CONFIG_PATH, "r", encoding="utf-8")) as f:
                    existing = await f.read()
                data = json.loads(existing)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.update(content)

        tmp_path = CONFIG_PATH.with_suffix(".tmp")
        async with (await anyio.open_file(tmp_path, "w", encoding="utf-8")) as f:
            await f.write(json.dumps(data, indent=4))
        
        os.replace(tmp_path, CONFIG_PATH)
        return True

async def async_read_config() -> dict:
    """
    Asynchronously reads the JSON config file in a concurrency-safe way.
    Returns an empty dict if the file doesn't exist or contains invalid JSON.
    """
    async with _config_lock:  # prevents read/write race conditions
        if not CONFIG_PATH.exists() or CONFIG_PATH.stat().st_size == 0:
            return {}

        try:
            async with (await anyio.open_file(CONFIG_PATH, "r", encoding="utf-8")) as f:
                content = await f.read()
            return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            # Corrupted or missing config — reset to empty
            return {}