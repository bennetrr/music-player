import asyncio
import logging
import sys
import urllib.request
from collections.abc import Callable, Coroutine
from typing import Any

from rich import print  # noqa: A004
from rich.table import Table
from textual_image.renderable import Image as CliImage

from music_player.core.constants import CONFIG_DIR
from music_player.core.music import ProviderPlugin, SearchResult
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
    """Register a function as a command."""
    commands[cmd_func.__name__] = cmd_func
    return cmd_func


search_result: SearchResult | None = None


def _render_search_result(_search_result: SearchResult) -> None:
    table = Table('ID', 'Image', 'Name', title='Artists')
    for i, artist in enumerate(_search_result.artists):
        img = (
            CliImage(urllib.request.urlretrieve(artist.cover_uri)[0], width='auto', height=4)
            if artist.cover_uri
            else None
        )
        table.add_row(str(i), img, artist.name)
    print(table)

    table = Table('ID', 'Image', 'Name', 'Year', 'Duration', 'Number of Tracks', title='Albums')
    for i, album in enumerate(_search_result.albums):
        img = (
            CliImage(urllib.request.urlretrieve(album.cover_uri)[0], width='auto', height=4)
            if album.cover_uri
            else None
        )
        table.add_row(
            str(i),
            img,
            album.name,
            str(album.year),
            f'{album.duration // 60}:{album.duration % 60:d}',
            str(album.number_of_tracks),
        )
    print(table)

    table = Table('ID', 'Image', 'Name', 'Duration', 'Number of Tracks', title='Playlists')
    for i, playlist in enumerate(_search_result.playlists):
        img = (
            CliImage(urllib.request.urlretrieve(playlist.cover_uri)[0], width='auto', height=4)
            if playlist.cover_uri
            else None
        )
        table.add_row(
            str(i),
            img,
            playlist.name,
            f'{playlist.duration // 60}:{playlist.duration % 60:d}',
            str(playlist.number_of_tracks),
        )
    print(table)

    table = Table('ID', 'Image', 'Name', title='Tracks')
    for i, track in enumerate(_search_result.tracks):
        img = (
            CliImage(urllib.request.urlretrieve(track.cover_uri)[0], width='auto', height=4)
            if track.cover_uri
            else None
        )
        table.add_row(str(i), img, track.title)
    print(table)


@command
async def search(query: str | None) -> None:
    """<query>   Search for music in TIDAL."""
    if not query:
        print('No query provided')
        return

    tidal = plugin_manager.get(ProviderPlugin, 'ing.ranft.bennet.tidal').instance()
    global search_result
    search_result = await tidal.search(query)
    _render_search_result(search_result)


@command
async def ls(inputs: str | None) -> None:
    """<type> <id>   List content in the music library."""
    if not inputs:
        print('No inputs provided')
        return

    if not search_result:
        print('You have to search first')
        return

    _type, _id = inputs.split(' ', 1)
    obj = search_result.__getattribute__(f'{_type}s')[int(_id)]

    tidal = plugin_manager.get(ProviderPlugin, 'ing.ranft.bennet.tidal').instance()
    res = await tidal.list(obj)
    _render_search_result(res)


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
