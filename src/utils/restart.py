import asyncio
import sys
import os

async def restart_app():
    print("\033[33mWARN\033[0m:     Restarting...(in 10 seconds)")
    await asyncio.sleep(10)  # Wait for 10 seconds before restarting
    python = sys.executable
    os.execv(python, [python] + sys.argv)