import asyncio
from asyncio import StreamReader, StreamWriter

import aioconsole
from utils import generate_data_vm, verify_password


class Client:
    def __init__(self):
        self.password = "pass"
        self.is_login = False
        self.vm_data = generate_data_vm()

    async def receive_messages(
        self, writer: StreamWriter, reader: StreamReader
    ):
        data = None
        while True:
            data = await reader.read(1024)
            if not data:
                break

            msg = data.decode()
            if msg.startswith("/auth"):
                password = msg.split("@")[-1]
                await self.auth(writer, password)
            elif not self.is_login:
                msg = (
                    "Сервер не может отдавать сообщения"
                    " или комады т.к не аунтефицирован"
                )
                writer.write(msg.encode())
            elif msg.startswith("/logout") and self.is_login:
                await self.logout(reader, writer)
            else:
                print(f"Ответ от сервера: {data.decode()}")
                await aioconsole.aprint("Введите сообщение для сервера: ")

    async def send_messages(self, writer: StreamWriter, reader: StreamReader):
        message = None
        while message != "exit":
            message: str = await aioconsole.ainput(
                "Введите сообщение для сервера: "
            )
            if message.startswith("/help"):
                await aioconsole.aprint(
                    "/update_vm - Отправляет на сервер "
                    "обновленные характеристики вм."
                )
            elif not self.is_login:
                await aioconsole.aprint(
                    "Вы не можете посылать команды серверу "
                    "который не был аунтефицирован с вм."
                )
            elif message.startswith("/update_vm"):
                await self.update(reader, writer)
            else:
                writer.write(message.encode())
                await writer.drain()
        else:
            writer.write()
            raise KeyboardInterrupt

    async def auth(self, writer: StreamWriter, password: str):
        if verify_password(self.password, password):
            self.is_login = True
            message = f"data@{self.vm_data}"
            writer.write(message.encode())
            await aioconsole.aprint("\r\033[KСервер аунтефицирован.")
            await aioconsole.aprint("Введите сообщение для сервера: ")
        else:
            message = (
                "Введен неккоректный пароль, "
                "данные о ВМ не могут быть получены."
            )
            writer.write(message.encode())
        await writer.drain()

    async def logout(self, reader: StreamReader, writer: StreamWriter):
        msg = "Сервер вышел из аунтефицированной ВМ"
        self.is_login = False
        await aioconsole.aprint(msg)
        writer.write("logout@".encode())

    async def update(self, reader: StreamReader, writer: StreamWriter):
        msg = "Обновление данных ВМ"
        self.vm_data = generate_data_vm()
        await aioconsole.aprint(msg)
        update_data = f"update@{self.vm_data}"
        writer.write(update_data.encode())

    async def start_client(self, host, port):
        reader, writer = await asyncio.open_connection(host, port)

        try:
            await asyncio.gather(
                self.receive_messages(writer, reader),
                self.send_messages(writer, reader),
            )
        except Exception as ex:
            raise ex
        finally:
            print("Соединение с сервером закрыто")
            writer.write(b"exit")
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    host = "127.0.0.1"
    port = "8001"

    client = Client()

    loop.run_until_complete(client.start_client(host, port))
