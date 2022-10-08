# import socket
# import json
# # Server
# s = socket.socket ()
# s.bind((socket.gethostname(), 8880))
# s.listen(5)
# client, addr = s.accept()
# print(s.recv(512).decode())


import asyncio
import json


# async def handle_echo(reader, writer):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')
#
#     print(f"Received {message!r} from {addr!r}")
#
#     txt_to_send =  {'response': 'pong'}
#     pong = json.dumps(txt_to_send)
#     print(f"Send: {pong!r}")
#     writer.write(pong.encode())
#     await writer.drain()
#
#     print("Close the connection")
#     writer.close()

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")
    message = json.loads(message)
    print(message['request'])


    txt_to_send = ''
    if message['request'] == 'ping':
        txt_to_send = {'response': 'pong'}
    elif message['request'] == 'play':
        move = input('move ?')
        txt_to_send = {
            "response": "move",
            "move": move,
            "message": "Fun message"
        }
    data = json.dumps(txt_to_send)
    writer.write(data.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 3333)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


# asyncio.run(main())