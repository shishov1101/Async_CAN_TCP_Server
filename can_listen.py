from typing import List
from server import CONNECTIONS
import can
import struct


async def send_to_connections(msg):
    size = 8
    for client in CONNECTIONS:
        client.write(msg.arbitration_id.to_bytes(4, byteorder='little'))
        client.write(len(msg.data).to_bytes(4, byteorder='little'))
        client.write(size.to_bytes(4, byteorder='little'))
        for i in range(size):
            if i >= len(msg.data):
                client.write((0).to_bytes(1, byteorder='little'))
            else:
                client.write(msg.data[i].to_bytes(1, byteorder='little'))
        client.write((0).to_bytes(4, byteorder='little'))
        ba = bytearray(struct.pack("f", msg.timestamp))
        for b in ba:
            client.write(b.to_bytes(1, byteorder='little'))


async def main(bus, loop, logs) -> None:
    if logs == 'ON':
        reader = can.AsyncBufferedReader()
        logger = can.Logger("logfile.asc")

        listeners: List = [
            reader,
            logger,
        ]
    else:
        reader = can.AsyncBufferedReader()

        listeners: List = [
            reader,
        ]
    notifier = can.Notifier(bus, listeners, loop=loop)
    while True:
        msg = await reader.get_message()
        await send_to_connections(msg)
    print("Done!")
    notifier.stop()