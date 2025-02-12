import asyncio
from uuid import UUID


async def client(auth_token: UUID):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write(str(auth_token).encode())
    await writer.drain()

    response = await reader.read(100)
    print(f"Server response: {response.decode()}")

    if response.decode() == "Authentication successful.":
        print("Connected to server.")
        # Логика отправки команд...
    else:
        print("Failed to connect to server.")

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    auth_token = UUID(
        "your_auth_token_here"
    )  # Токен, полученный при создании виртуальной машины
    asyncio.run(client(auth_token))
