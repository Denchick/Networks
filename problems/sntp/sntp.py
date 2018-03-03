import socket
import struct
import collections
import random
import datetime
import sys
import concurrent.futures as cf
from threading import Thread
import argparse

PORT = 123
LOCALHOST = '127.0.0.1'
BYTES_IN_LINE = 16
SEPARATOR = '   '
R_FRAME_STRUCT = '!BBBBiI4B2I2I2I2I'
OUT_FRAME = '!BBBBiII4Q'
MY_STRATUM = 3
MY_ID = (235, 80, 141, 90)
MY_PRECISION = 210
MY_DELAY = 10000
VERSION = 4
SERVER_MODE = 4
NTP_UTC_OFFSET = 2208988800


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.settimeout(1 / 60)

server_socket.bind(('', PORT))

frame_queue = collections.deque([])

exception = 'All right'

done = 0


def process_frame():
    while not done:
        try:
            frame_data, address = server_socket.recvfrom(1024)
            print('received from', address)
        except socket.timeout:
            continue

        unpacked = struct.unpack(R_FRAME_STRUCT, frame_data)
        frame = collections.OrderedDict()
        flags = unpacked[0]
        frame['leap'] = int(('0'*8 + bin(flags)[2:])[-8:][:2], 2)
        frame['ver'] = int(('0'*8 + bin(flags)[2:])[-8:][2:5], 2)
        frame['mode'] = int(('0'*8 + bin(flags)[2:])[-8:][5:], 2)
        frame['stratum'] = unpacked[1]
        frame['poll'] = unpacked[2]
        frame['precision'] = unpacked[3]
        frame['root_delay'] = unpacked[4]
        frame['root_disp'] = unpacked[5]
        frame['ref_id'] = unpacked[6:10]
        frame['ref_ts'] = unpacked[10:12]
        frame['orig_ts'] = unpacked[12:14]
        frame['recv_ts'] = unpacked[14:16]
        frame['trans_ts'] = unpacked[16:18]
        frame_queue.append((frame, address))


def reply(frame, reply_addr, time_shift):
    try:
        cur_time = datetime.datetime.now().timestamp() +\
                   NTP_UTC_OFFSET + time_shift

        leap = frame['leap']
        version = VERSION
        mode = SERVER_MODE
        flags =\
            (leap << 6) + (version << 3) + mode

        stratum = MY_STRATUM
        poll = frame['poll']
        precision = MY_PRECISION
        root_delay = MY_DELAY
        root_disp = random.randint(0, 1024)

        ref_id = 0
        shifter = 24
        for x in MY_ID:
            ref_id += (x << shifter)
            shifter -= 8

        ref_id = ref_id
        ref_ts =\
            (int(cur_time) << 32) + int((cur_time - int(cur_time))*10e3)

        recv_ts =\
            (int(cur_time) << 32) +\
            int((cur_time - int(cur_time))*10e6)

        cur_time = datetime.datetime.now().timestamp() +\
                   NTP_UTC_OFFSET + time_shift
        trans_ts =\
            (int(cur_time) << 32) + int((cur_time - int(cur_time))*10e6)

        orig_ts = (frame['trans_ts'][0] << 32) + frame['trans_ts'][1]

        returned_frame = struct.pack(OUT_FRAME,
                                     flags, stratum, poll, precision,
                                     root_delay, root_disp, ref_id,
                                     ref_ts, orig_ts, recv_ts, trans_ts)
    except Exception as e:
        global exception
        exception = e

    with socket.socket(type=socket.SOCK_DGRAM) as reply_socket:
        try:
            reply_socket.sendto(returned_frame, reply_addr)
            print('sent to ', reply_addr)
        except Exception as e:
            print(e)

recv_thread = Thread(target=process_frame)

parser = argparse.ArgumentParser()
parser.add_argument('time_shift', nargs='?', type=int, default=0)

args = parser.parse_args()

try:
    recv_thread.start()
    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        while 1:
            if frame_queue:
                print('queue has elements')
                ext_frame, addr = frame_queue.popleft()
                executor.submit(reply, ext_frame, addr, args.time_shift)

except KeyboardInterrupt:
    done = 1
    recv_thread.join(3)
    server_socket.close()
