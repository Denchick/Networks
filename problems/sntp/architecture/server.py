import socket
import struct
from datetime import datetime
import random
import sys
import asyncio
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1 / 60)
        self.socket.bind(('', 123))
        logging.info('Connection is established')

    def handle_datagram(self, data, address):
        logging.debug(f'Received request from {address}')
        message_format = MessageFormat(data)
        logging.debug(f'Parse received data to MessageFormat {address}')
        response_message = self.create_response_message(message_format)
        logging.debug(f'Create response message')
        self.transport.sendto(response_message, address)
        logging.debug(f'Send response to {address}')

    def create_response_message(self, message_format):
        current_time = datetime.now().timestamp() + NTP_UTC_OFFSET + self.time_shift

        leap = message_format.leap
        version = VERSION
        mode = SERVER_MODE
        first_byte =(leap << 6) + (version << 3) + mode
        stratum = STRATUM
        poll = message_format.poll
        precision = PRECISION
        root_delay = DELAY
        root_dispersion = random.randint(0, 1024)
        ref_id = 0
        shifter = 24
        for x in ID:
            ref_id += (x << shifter)
            shifter -= 8

        ref_id = ref_id
        ref_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e3)

        recv_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e6)

        current_time = datetime.now().timestamp() + NTP_UTC_OFFSET + self.time_shift
        trans_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e6)

        orig_ts = (message_format.transmit_timestamp[0] << 32) + \
                  message_format.transmit_timestamp[1]

        return struct.pack('!BBBBiII4Q',
                           first_byte, stratum, poll, precision,
                           root_delay, root_dispersion, ref_id,
                           ref_ts, orig_ts, recv_ts, trans_ts)

    def start(self):
        self.create_connection()
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                print('received from', address)
            except socket.timeout:
                continue
            with socket.socket(type=socket.SOCK_DGRAM) as reply_socket:
                try:
                    response = self.create_response_message(MessageFormat(data))
                    reply_socket.sendto(response, address)
                    print('sent to ', address)
                except Exception as e:
                    print(e)

    def stop(self):
        self.socket.close()