from .database import get_collection
import os
import sys
sys.path.insert(1, os.getcwd())
import src.settingsmanager as settingsmanager

async def ensure_indexes():
    try:
        setup_complete = settingsmanager.read_config().get("global").get("setup_complete")  # pyright: ignore[reportOptionalMemberAccess]
    except AttributeError:
        setup_complete = False
    if setup_complete:
        users = await get_collection("users")
        await users.create_index("email", unique=True)
        await users.create_index("username", unique=True)
        await users.create_index("sub", unique=True)
    else:
        print("\033[32mINFO\033[0m:     Skipping index creation as setup is not complete...")