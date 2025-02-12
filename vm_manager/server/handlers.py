from server.schemas import VirtualMachineSchemaDB
from server.db import create_pool, authenticate_vm


async def client_handler(reader, writer):
    auth_token = (await reader.read(100)).decode().strip()
    pool = await create_pool()

    vm_record = await authenticate_vm(pool, auth_token)

    if vm_record:
        vm = VirtualMachineSchemaDB(
            id=vm_record["id"],
            ram_gb=vm_record["ram_gb"],
            cpu_count=vm_record["cpu_count"],
            auth_token=vm_record["auth_token"],
            is_online=True,
        )
        print(f"VM {vm.id} authenticated.")
        writer.write(b"Authentication successful.")
        await writer.drain()

        # Обработка команд клиента
        while True:
            data = await reader.read(100)
            if not data:
                break
            command = data.decode().strip()
            print(f"Received command: {command}")
            # Логика обработки команд...
    else:
        writer.write(b"Authentication failed.")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
