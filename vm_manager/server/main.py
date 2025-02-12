import asyncio
from server.handlers import client_handler


async def run_server(host: str, port: str):
    server = await asyncio.start_server(client_handler, host, port)
    async with server:
        print("Server started on 127.0.0.1:8888")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())
