import argparse
import can_listen
import asyncio
import server
import can
from sys import platform
import os


parser = argparse.ArgumentParser(description='Parameters for Server.')
print(platform)
if platform == "linux" or platform == "linux2":
    parser.add_argument('-c', '--can',  help='Port required for use', metavar='CanN', type=str, default='can0')
elif platform == "win32":
    parser.add_argument('-c', '--can',  help='Port required for use', type=str, default='PCAN_USBBUS1')
else:
    print("This OS not support by this script")
    exit(-1)
parser.add_argument('-l', '--logs', help='The type of radar used', choices=['ON', 'OFF'], default='OFF')
parser.add_argument('-p', '--port', help='The value of TCP server port', type=int, default=8020)


args = parser.parse_args()

print("CAN interface:             ", args.can)
print("Logger level:              ", args.logs)
print("Logger level:              ", args.port)


async def main(bus, port):
    loop = asyncio.get_running_loop()
    task1 = asyncio.create_task(can_listen.main(bus, loop, args.logs))
    task2 = asyncio.create_task(server.main(port, bus, loop))
    await asyncio.gather(task2, task1)

try:
    if platform == "linux" or platform == "linux2":
        channelStr = os.environ.get('CAN_PORT', args.can)
        bus = can.interface.Bus(bustype='socketcan', channel=channelStr, bitrate=500000)
        asyncio.run(main(bus, port=args.port))
    elif platform == "win32":
        bus = can.interface.Bus(bustype="pcan", channel=args.can, bitrate=500000)
        asyncio.run(main(bus, port=args.port))
except:
    print("Server finished execution")
    exit(-1)
