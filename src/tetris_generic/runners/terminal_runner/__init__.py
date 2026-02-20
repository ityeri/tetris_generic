from argparse import ArgumentParser

from .terminal_runner import TerminalRunner
from .formatted_text_surface import FormattedTextSurface
from .key_map import KeyMap

from tetris_generic.default_impl import DEFAULT_SPACE_WIDTH, DEFAULT_SPACE_HEIGHT


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-w', '--width', help='Width of gamespace',
        default=str(DEFAULT_SPACE_WIDTH), nargs='?'
    )
    parser.add_argument(
        '-v', '--height', help='Height of gamespace',
        default=str(DEFAULT_SPACE_HEIGHT), nargs='?'
    )
    parser.add_argument(
        '-i', '--interval', help='Interval of each tick (seconds, can be float)',
        default='0.5', nargs='?'
    )
    parser.add_argument(
        '-q', '--que-length', help='Length of next tetrominos que',
        default='5', nargs='?'
    )

    args = parser.parse_args()

    runner = TerminalRunner(
        width=int(args.width),
        height=int(args.height),
        interval=float(args.interval),
        que_length=int(args.que_length),
    )
    runner.run()

__all__ = [
    'main',
    'TerminalRunner',
    'FormattedTextSurface',
    'KeyMap'
]