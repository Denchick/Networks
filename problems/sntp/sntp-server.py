#!/usr/bin/env python3
import argparse
import asyncio
import sys
from architecture.server import SNTPServer
import logging

__version__ = '1.1'
__author__ = 'Volkov Denis'
__group__ = 'FIIT-201'


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description=""" Сервер точного времени, который «врет» на заданное число секунд. """)
    parser.add_argument(
        '-t', '--time-shift', type=int, default=0,
        help=""" Смещение времени, на которое "врет" сервер """)
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Печатает версию утилиты и выходит.")

    return parser.parse_args()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    args = create_parser()

    if args.version:
        print(__version__)
        sys.exit()

    server = SNTPServer('localhost', 123, args.time_shift)
    try:
        server.start()
    except KeyboardInterrupt:
        logging.debug("Keyboard interrupt.")
    except Exception as e:
        print(e)
    finally:
        server.stop()
        sys.exit()