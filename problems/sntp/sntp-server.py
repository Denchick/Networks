#!/usr/bin/env python3
import argparse
import asyncio
import sys
from architecture.server import SNTPServer
import logging

__version__ = '1.1'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description=""" Сервер точного времени, который «врет» на заданное число секунд. """)
    parser.add_argument(
        '-s', '--server', type=str, default='',
        help=""" Сервер, у которого этот сервер узнает точное время""")
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

    logging.debug("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    server = SNTPServer('localhost', 123)
    try:
        server.start()
    except KeyboardInterrupt:
        logging.debug("Keyboard interrupt.")
    except Exception as e:
        print(e)
    finally:
        server.stop()
        sys.exit()