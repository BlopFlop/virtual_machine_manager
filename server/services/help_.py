from aioconsole import aprint
from core.constants import HELP_MSG


async def get_help():
    """Show help message."""
    await aprint(HELP_MSG)
