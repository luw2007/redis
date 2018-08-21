"""
redis proxy
用来展示redis协议
"""
import asyncio

redis_addr = ('127.0.0.1', 6379)
proxy_addr = ('127.0.0.1', 6380)


async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.read(1024)
            print(data)
            writer.write(data)
    finally:
        writer.close()


async def handle_client(local_reader, local_writer):
    try:
        remote_reader, remote_writer = await asyncio.open_connection(
            *redis_addr)
        send_pipe = pipe(local_reader, remote_writer)
        recv_pipe = pipe(remote_reader, local_writer)
        await asyncio.gather(send_pipe, recv_pipe)
    finally:
        local_writer.close()


if __name__ == "__main__":
    # Create the server
    loop = asyncio.get_event_loop()

    coro = asyncio.start_server(handle_client, *proxy_addr)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    loop.run_forever()
    loop.close()
