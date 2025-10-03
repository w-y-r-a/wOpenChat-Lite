import asyncio
import sys
import os

async def restart_app():
    print("\033[33mWARN\033[0m:     Restarting...(in 10 seconds)")
    await asyncio.sleep(1)  # Wait for 1 second before restarting
    python = sys.executable
    os.execv(python, [python] + sys.argv)