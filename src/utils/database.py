from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
import sys
sys.path.insert(1, os.getcwd())
import src.settingsmanager as settingsmanager # pylint: disable=import-error

db = None
client = None


async def init_db():
    """
    Initializes the MongoDB connection.
    This function creates an asynchronous MongoDB client and verifies the connection
    by sending a ping command. It sets the global `client` and `db` variables for use
    throughout the application.
    Returns:
        bool: True if the connection is successful, otherwise raises an exception.
    """
    try:
        setup_complete = settingsmanager.read_config().get("global").get("setup_complete")  # pyright: ignore[reportOptionalMemberAccess]
    except AttributeError:
        setup_complete = False
    if not setup_complete:
        print("\033[32mINFO\033[0m:     Setup not complete!")
        return False
    print("\033[32mINFO\033[0m:     Setup Complete!")
    MONGO_URL = settingsmanager.read_config().get("mongo_url")
    if not MONGO_URL:
        raise ValueError("\033[31mERROR\033[0m:     Missing 'mongo_url' in config.")
    global client, db
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            maxPoolSize=50,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            waitQueueTimeoutMS=5000,
        )

        await client.admin.command("ping")
        print("\033[32mINFO\033[0m:     Connected to MongoDB!")
        db = client["wOpenChat"]

        return True
    except ConnectionFailure as e:
        raise Exception(f"\033[31mERROR\033[0m:     Failed to connect to MongoDB: {str(e)}") from e

async def get_collection(collection_name: str):
    global db
    if db is None:
        ok = await init_db()
        if not ok or db is None:
            raise RuntimeError("Database is not initialized; call init_db() after completing setup.")
    return db[collection_name]  # pyright: ignore[reportOptionalSubscript]

# Doesn't need to be async since it's just closing the connection
def close_db_connection():
    """
    Closes the MongoDB and Redis connections if they are open.

    This function asynchronously closes the MongoDB client and Redis connection,
    resetting their global references to None.
    """
    global client
    if client:
        print("\033[32mINFO\033[0m:     Closing MongoDB connection...")
        client.close()
        print("\033[32mINFO\033[0m:     MongoDB connection closed.")
        client = None

async def test_db_connection(URL) -> bool:
    """
    Tests the MongoDB connection by sending a ping command.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    client = AsyncIOMotorClient(
        URL,
        maxPoolSize=50,
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000,
        waitQueueTimeoutMS=5000,
    )
    try:
        await client.admin.command("ping")
        print("\033[32mINFO\033[0m:     MongoDB connection test successful!")
        return True
    except ConnectionFailure as e:
        print(f"\033[31mERROR\033[0m:     MongoDB connection test failed: {e!s}")
        return False