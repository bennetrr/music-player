import asyncio
import logging
import sys
import urllib.request
from collections.abc import Callable, Coroutine
from typing import Any

from rich import print  # noqa: A004
from rich.table import Table, Column
from textual_image.renderable import Image as CliImage

from music_player.core.constants import CONFIG_DIR
from music_player.core.music import ProviderPlugin
from music_player.core.plugin_manager import plugin_manager

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s: %(levelname)s | %(name)s] %(message)s', '%H:%M:%S')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

logger = logging.getLogger('music_player.core.main')

type Command = Callable[[str | None], Coroutine[Any, Any, None]]
commands: dict[str, Command] = {}


def command(cmd_func: Command) -> Command:
    """Decorator for registering a command."""
    commands[cmd_func.__name__] = cmd_func
    return cmd_func


@command
async def search(query: str | None) -> None:
    """Search for a track."""
    print(f'Searching for "{query}"...')
    tidal = plugin_manager.get(ProviderPlugin, 'ing.ranft.bennet.tidal').instance()

    if not query:
        print('No query provided')
        return

    res = await tidal.search(query)

    table = Table('Image', 'Name', Column('ID', no_wrap=True), title='Artists')
    for artist in res.artists:
        img = (
            CliImage(urllib.request.urlretrieve(artist.cover_uri)[0], width='auto', height=4)
            if artist.cover_uri
            else None
        )
        table.add_row(img, artist.name, artist.id)
    print(table)

    table = Table('Image', 'Name', 'Year', 'Duration', 'Number of Tracks', Column('ID', no_wrap=True), title='Albums')
    for album in res.albums:
        img = (
            CliImage(urllib.request.urlretrieve(album.cover_uri)[0], width='auto', height=4)
            if album.cover_uri
            else None
        )
        table.add_row(
            img,
            album.name,
            str(album.year),
            f'{album.duration // 60}:{album.duration % 60:d}',
            str(album.number_of_tracks),
            album.id,
        )
    print(table)

    table = Table('Image', 'Name', 'Duration', 'Number of Tracks', Column('ID', no_wrap=True), title='Playlists')
    for playlist in res.playlists:
        img = (
            CliImage(urllib.request.urlretrieve(playlist.cover_uri)[0], width='auto', height=4)
            if playlist.cover_uri
            else None
        )
        table.add_row(
            img,
            playlist.name,
            f'{playlist.duration // 60}:{playlist.duration % 60:d}',
            str(playlist.number_of_tracks),
            playlist.id,
        )
    print(table)

    table = Table('Image', 'Name', Column('ID', no_wrap=True), title='Tracks')
    for track in res.tracks:
        img = (
            CliImage(urllib.request.urlretrieve(track.cover_uri)[0], width='auto', height=4)
            if track.cover_uri
            else None
        )
        table.add_row(img, track.title, track.id)
    print(table)


async def main() -> None:
    """Main entry point of the application."""
    logger.info('Starting music player...')
    logger.info('Config directory: "%s"', CONFIG_DIR)

    with plugin_manager:
        plugin_manager.load_plugins()

        tidal = plugin_manager.get(ProviderPlugin, 'ing.ranft.bennet.tidal').instance()
        login_result = await tidal.login()

        if login_result.result is True:
            logger.info('Successfully logged in')
        elif login_result.result is False:
            logger.error('Failed to log in')
        else:
            for strategy in login_result.strategies:
                logger.info('%s', strategy)

            result = await login_result.result

            if result:
                logger.info('Successfully logged in')
            else:
                logger.error('Failed to log in')

        while True:
            cmd = input('> ').split(' ', 1)

            if cmd[0] in ('exit', 'quit', 'e', 'q'):
                break

            if cmd[0] in ('help', 'h') or cmd[0] not in commands:
                print('Available commands:')
                for cmd_name, cmd_func in commands.items():
                    print(f'  {cmd_name}: {cmd_func.__doc__}')
                print('help | h: Show this help message')
                print('exit | quit | e | q: Exit the application')
                continue

            await commands[cmd[0]](cmd[1] if len(cmd) > 1 else None)


if __name__ == '__main__':
    asyncio.run(main())
