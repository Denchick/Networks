import random
import struct
import collections

from datetime import datetime

STRATUM = 3
ID = (235, 80, 141, 90)
PRECISION = 210
DELAY = 10000
VERSION = 4
SERVER_MODE = 4
NTP_UTC_OFFSET = 2208988800

class MessageFormat:

    def __init__(self, binary_data):
        unpacked = struct.unpack('!BBBBiI4B2I2I2I2I', binary_data) # WTF?
        message = collections.OrderedDict()
        first_byte = unpacked[0]
        message['leap'] = first_byte & (2**7 + 2**6)
        message['version'] = first_byte & (2**5 + 2**4 + 2**3)
        message['mode'] = first_byte & (2**2 + 2**1 + 2**0)     
        message['stratum'] = unpacked[1]
        message['poll'] = unpacked[2]
        message['precision'] = unpacked[3]
        message['root_delay'] = unpacked[4]
        message['root_disp'] = unpacked[5]
        message['ref_id'] = unpacked[6:10]
        message['ref_ts'] = unpacked[10:12]
        message['orig_ts'] = unpacked[12:14]
        message['recv_ts'] = unpacked[14:16]
        message['trans_ts'] = unpacked[16:18]

        self._data = message
    
    @property
    def leap(self):
        return self._data['leap']

    @property
    def poll(self):
        return self._data['poll']

    @property
    def transmit_timestamp(self):
        return self._data['trans_ts']

    @staticmethod
    def pack_message(leap, poll, transmit_timestamp, time_shift):
        current_time = datetime.now().timestamp() + NTP_UTC_OFFSET + time_shift
        first_byte =(leap << 6) + (VERSION << 3) + SERVER_MODE
        root_dispersion = random.randint(0, 1024)
        ref_id = 0
        shifter = 24
        for x in ID:
            ref_id += (x << shifter)
            shifter -= 8
        ref_id = ref_id
        ref_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e3)
        recv_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e6)
        current_time = datetime.now().timestamp() + NTP_UTC_OFFSET + time_shift
        trans_ts = (int(current_time) << 32) + int((current_time - int(current_time))*10e6)
        orig_ts = (transmit_timestamp[0] << 32) + transmit_timestamp[1]

        return struct.pack('!BBBBiII4Q',
                           first_byte, STRATUM, poll, PRECISION,
                           DELAY, root_dispersion, ref_id,
                           ref_ts, orig_ts, recv_ts, trans_ts)