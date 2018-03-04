import struct
import collections

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
