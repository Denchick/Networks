import collections
import socket
import logging
import threading
import concurrent.futures as cf
from architecture.message_format import MessageFormat

STRATUM = 3
ID = (235, 80, 141, 90)
PRECISION = 210
DELAY = 10000
VERSION = 4
SERVER_MODE = 4
NTP_UTC_OFFSET = 2208988800

class SNTPServer():

    def __init__(self, host, port, time_shift=0):
        self.host = host
        self.port = port
        self.time_shift = time_shift
        self.message_queue = collections.deque([])
        self.create_connection()
        self.is_working = True

    def create_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1 / 60)
        self.socket.bind(('', 123))
        logging.info('Connection is established')

    def receive_data(self):
        while self.is_working:
            try:
                data, address = self.socket.recvfrom(1024)
                logging.debug(f'Received request from {address}')
                message_format = MessageFormat(data)
                logging.debug(f'Parse received data to MessageFormat {address}')
                response = MessageFormat.pack_message(message_format.leap,
                                                      message_format.poll,
                                                      message_format.transmit_timestamp,
                                                      self.time_shift)
                logging.debug(f'Create response message')
                self.message_queue.append(response)
                logging.debug('Add message to queue')
            except socket.timeout:
                logging.debug(f'Socket timeout')
                continue
            except Exception as e:
                logging.error(f'Exception: {e}')

    def send_data(self):
        message, address = self.message_queue.popleft()
        with socket.socket(type=socket.SOCK_DGRAM) as reply_socket:
            try:
                reply_socket.sendto(message, address)
                logging.debug(f'Send reply to {address}')
            except Exception as e:
                print(e)

    def start(self):
        receiver = threading.Thread(target=self.receive_data, args=(self))
        try:
            logging.debug('Start receive thread.')
            receiver.start()
            logging.debug('Start send pool.')
            with cf.ThreadPoolExecutor(max_workers=5) as executor:
                while self.is_working and self.message_queue:
                    logging.debug('Queu
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
        self.is_working = False