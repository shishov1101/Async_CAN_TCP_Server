import asyncio
import can


CONNECTIONS = list()
collect_messages = list()


class CanServerProtocol(asyncio.Protocol):
    def __init__(self, bus):
        self.transport = None
        self.bus = bus

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        CONNECTIONS.append(self.transport)

    def data_received(self, data):
        standard_size = 84
        if len(data) % standard_size == 0:
            message_length = (len(data)) / standard_size
            for j in range(int(message_length)):
                id_message = bytearray(b'')
                size = bytearray(b'')
                data_message = bytearray(b'')
                for i in range(4):
                    id_message += data[i + j * standard_size].to_bytes(1, byteorder='little')
                    size += data[4 + i + j * standard_size].to_bytes(1, byteorder='little')
                id_message = int.from_bytes(id_message, 'little')
                size = int.from_bytes(size, 'little')
                for i in range(size):
                    data_message += data[i + 12 + j * standard_size].to_bytes(1, byteorder='little')
                collect_messages.append(can.Message(arbitration_id=id_message, data=data_message, is_extended_id=False))
            for msg in collect_messages:
                try:
                    self.bus.send(msg)
                except self.bus.CanError:
                    print("Error! Message did not send")
        else:
            print("Server received not CAN Message")

    def connection_lost(self, exc):
        print('The server closed the connection ', self.transport.get_extra_info('peername'))
        CONNECTIONS.remove(self.transport)


async def main(port, bus, loop):
    server = await loop.create_server(
        lambda: CanServerProtocol(bus),
        'localhost', port)
    async with server:
        await server.serve_forever()