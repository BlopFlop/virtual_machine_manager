import asyncio
import logging
from asyncio import StreamReader, StreamWriter

from aioconsole import ainput
from core.constants import (
    AUTH,
    CLIENTS,
    DATE_FORMAT,
    HD_LIST,
    HELP,
    LOG_FORMAT,
    LOGOUT,
    MESSAGE,
    VM_ALL,
    VM_AUTH,
    VM_ONLINE,
)
from core.logging_ import configure_logging
from services import (
    add_vm,
    auth_vm,
    get_auth_vm,
    get_clients,
    get_online_vm,
    get_vm,
    logout_vm,
    offline_vm,
    update_auth_vm,
)
from services.hd import get_hd
from services.help_ import get_help
from utils import get_password_hash


class Client:
    def __init__(self, writer: StreamWriter):
        self.writer = writer
        self.is_auth = False
        self.vm_id = None

    @property
    def address(self) -> str:
        """Get addres."""
        addr, port = self.writer.get_extra_info("peername")
        return f"{addr}:{port}"


class Server:
    NOT_ARG_COMMANDS = {
        VM_ONLINE: get_online_vm,
        VM_AUTH: get_auth_vm,
        VM_ALL: get_vm,
        HD_LIST: get_hd,
        HELP: get_help,
    }

    def __init__(self):
        self.clients: dict[str:Client] = {}

    async def _get_client(self, full_addr: str) -> Client:
        if full_addr not in self.clients:
            logging.warning(f"Данный клиент не онлайн {full_addr}")
            return
        return self.clients[full_addr]

    async def command_send_msg(self, args: list[str]):
        """Send message for client."""

        if len(args) < 2:
            logging.warning("Неккорекнтые аргументы")
            return
        addr, *msg = args
        msg = " ".join(msg)
        client = await self._get_client(addr)
        if not client:
            return
        logging.info(f"Команда {msg} отправлена клиенту {client.address}")
        client.writer.write(msg.encode())
        await client.writer.drain()

    async def command_clients(self):
        """Get all online clients."""
        get_clients(self.clients)

    async def command_auth_client(self, args: list[str]):
        """Auth clients."""
        if len(args) < 2:
            logging.warning("Неккорекнтые аргументы")
            return
        addr, password, *_ = args
        client = await self._get_client(addr)
        if not client:
            return
        logging.info(
            f"Запрос на аунтефикацию отправлен клиенту {client.address}"
        )
        password = "/auth@" + get_password_hash(password)
        client.writer.write(password.encode())

    async def command_logout_client(self, args: list[str]):
        """Logout clients."""
        if not args:
            logging.warning("Неккорекнтые аргументы")
            return
        addr, *_ = args
        client = await self._get_client(addr)
        if not client:
            return
        logging.info(f"Запрос на выход из авторизованной ВМ {client.address}")
        client.writer.write(b"/logout")

    async def console_handler(self):
        """Serever inner command."""
        while True:
            command: str = await ainput(">> ")
            command, *args = command.strip().split()

            if command in self.NOT_ARG_COMMANDS:
                await self.NOT_ARG_COMMANDS[command]()
            elif command == AUTH:
                await self.command_auth_client(args)
            elif command == LOGOUT:
                await self.command_logout_client(args)
            elif command == MESSAGE:
                await self.command_send_msg(args)
            elif command == CLIENTS:
                await self.command_clients()
            else:
                logging.warning("Команда не распознана")

    async def receive_messages(self, reader: StreamReader, client: Client):
        """Client outer command handler."""
        msg = None
        while msg != "exit":
            data = await reader.read(2048)
            if not data:
                break

            msg = data.decode().strip()

            if msg.startswith("data@"):
                data_vm = msg.split("@")[-1]

                if client.vm_id is None:
                    vm_id = await add_vm(data_vm)
                    client.vm_id = vm_id

                await auth_vm(client.vm_id)
                client.is_auth = True
            elif msg.startswith("logout@"):
                if client.is_auth:
                    client.is_auth = False
                    await logout_vm(client.vm_id)
            elif msg.startswith("update@"):
                update_data_vm = msg.split("@")[-1]
                await update_auth_vm(
                    vm_id=client.vm_id, vm_data=update_data_vm
                )
            else:
                logging.info(f"Получено от {client.address}: {msg}")
        if client.is_auth and not (client.vm_id is None):
            client.is_auth = False
            await offline_vm(client.vm_id)
        self.clients.pop(client.address)

    async def client_handler(self, reader: StreamReader, writer: StreamWriter):
        """Client handler."""
        addr, port = writer.get_extra_info("peername")
        full_addr = f"{addr}:{port}"
        logging.info(f"Подключен клиент: {addr}:{port}")
        client = Client(writer)
        self.clients[full_addr] = client

        await self.receive_messages(reader, client)

        logging.info(f"Клиент {addr} отключен")
        writer.close()
        await writer.wait_closed()

    async def start_server(self, host: str, port: str) -> None:
        """Start server."""
        server = await asyncio.start_server(
            self.client_handler, host=host, port=port
        )

        address = server.sockets[0].getsockname()
        logging.info(f"Сервер запущен на {address}")

        async with server:
            await asyncio.gather(
                server.serve_forever(), self.console_handler()
            )


if __name__ == "__main__":
    configure_logging(DATE_FORMAT, LOG_FORMAT)

    host = "127.0.0.1"
    port = "8001"

    server = Server()
    asyncio.run(server.start_server(host, port))
