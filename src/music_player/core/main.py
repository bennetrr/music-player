import asyncio
import logging
import sys

from music_player.core.plugin_manager import load_plugins

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s: %(levelname)s | %(name)s] %(message)s', '%H:%M:%S')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

logger = logging.getLogger('music_player.core.main')


async def main() -> None:
    """Main entry point of the application."""
    logger.info('Starting music player...')
    load_plugins()


if __name__ == '__main__':
    asyncio.run(main())
