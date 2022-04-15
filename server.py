import asyncio
import can


CONNECTIONS = list()


class CanServerProtocol(asyncio.Protocol):
    def __init__(self, bus):
        self.transport = None
        self.bus = bus
        self.id_message = bytearray(b'')
        self.size = bytearray(b'')
        self.data_message = bytearray(b'')

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        CONNECTIONS.append(self.transport)

    def data_received(self, data):
        message_length = (len(data)) / 84
        for j in range(int(message_length)):
            for i in range(4):
                self.id_message += data[i + j * 84].to_bytes(1, byteorder='little')
                self.size += data[4 + i + j * 84].to_bytes(1, byteorder='little')
            self.id_message = int.from_bytes(self.id_message, 'little')
            self.size = int.from_bytes(self.size, 'little')
            for i in range(self.size):
                self.data_message += data[i + 12 + j * 84].to_bytes(1, byteorder='little')
            try:
                self.bus.send(can.Message(arbitration_id=self.id_message, data=self.data_message, is_extended_id=False))
            except self.bus.CanError:
                print("Error! Message did not send")
            self.id_message = bytearray(b'')
            self.size = bytearray(b'')
            self.data_message = bytearray(b'')

    def connection_lost(self, exc):
        print('The server closed the connection ', self.transport.get_extra_info('peername'))
        CONNECTIONS.remove(self.transport)


async def main(port, bus, loop):
    server = await loop.create_server(
        lambda: CanServerProtocol(bus),
        'localhost', port)
    async with server:
        await server.serve_forever()