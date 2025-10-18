import asyncio
import sys
import os

async def restart_app():
    print("\033[33mWARN\033[0m:     Restarting...(in 1 seconds)")
    await asyncio.sleep(1)
    python = sys.executable
    os.execv(python, [python] + sys.argv)