import argparse
import can_listen
import asyncio
import server
import can


parser = argparse.ArgumentParser(description='Parameters for Server.')
parser.add_argument('-c', '--can', help='Can interface', metavar='PCAN_USBBUSN',
                    type=str, default='PCAN_USBBUS1')
parser.add_argument('-l', '--loglevel', help='The type of radar used',
                    choices=['DEBUG', 'INFO', 'ERROR'], default='DEBUG')


args = parser.parse_args()

print("CAN interface:             ", args.can)
print("Logger level:              ", args.loglevel)


async def main():
    port = 8020
    bus = can.Bus(interface="pcan", channel="PCAN_USBBUS1")
    loop = asyncio.get_running_loop()
    task1 = asyncio.create_task(can_listen.main(bus, loop))
    task2 = asyncio.create_task(server.main(port, bus, loop))
    await asyncio.gather(task2, task1)

asyncio.run(main())
