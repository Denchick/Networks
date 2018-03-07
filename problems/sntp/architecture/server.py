import socket
import logging
from architecture.message_format import MessageFormat

STRATUM = 3
ID = (235, 80, 141, 90)
PRECISION = 210
DELAY = 10000
VERSION = 4
SERVER_MODE = 4
NTP_UTC_OFFSET = 2208988800

class SNTPServer:

    def __init__(self, host, port, time_shift=0):
        self.host = host
        self.port = port
        self.time_shift = time_shift

    def create_connection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(1 / 60)
            self.socket.bind(('', 123))
            logging.info('Connection is established')
        except

    def start(self):
        self.create_connection()
        logging.debug("Starting SNTP server")
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                logging.debug(f'Received request from {address}')
            except socket.timeout:
                continue
            with socket.socket(type=socket.SOCK_DGRAM) as reply_socket:
                try:
                    message_format = MessageFormat(data)
                    logging.debug(f'Parse received data to MessageFormat {address}')
                    response = MessageFormat.pack_message(message_format.leap,
                                                          message_format.poll,
                                                          message_format.transmit_timestamp,
                                                          self.time_shift)
                    logging.debug(f'Create response message')
                    reply_socket.sendto(response, address)
                    logging.debug(f'Send response to {address}')
                except Exception as e:
                    print(e)

    def stop(self):
        self.socket.close()