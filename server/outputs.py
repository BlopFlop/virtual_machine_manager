from models import HDSchemaDB, VMSchemaDB
from prettytable import PrettyTable


def pretty_clients_output(clients: dict) -> None:
    """Clients table output."""
    output_table = PrettyTable()
    output_table.field_names = ("addr", "is_auth")
    output_table.align = "l"

    for client in clients.values():
        rows = (client.address, client.is_auth)
        output_table.add_row(rows)
    print(output_table)


def pretty_vm_output(vm_objs: list[VMSchemaDB]) -> None:
    """Virtual machine table output."""
    output_table = PrettyTable()
    output_table.field_names = (
        "id",
        "ram_amount",
        "cpu_amount",
        "rom_amount",
        "is_online",
        "is_auth",
    )
    output_table.align = "l"
    for vm_obj in vm_objs:
        rom_amount = 0
        if vm_obj.hard_drives:
            rom_amount = sum(map(lambda hd: hd.rom_amount, vm_obj.hard_drives))
        rows = (
            vm_obj.id,
            vm_obj.ram_amount,
            vm_obj.cpu_amount,
            rom_amount,
            vm_obj.is_online,
            vm_obj.is_auth,
        )
        output_table.add_row(rows)
    print(output_table)


def pretty_hd_output(hd_objs: list[HDSchemaDB]) -> None:
    """Hard Drives table output."""
    output_table = PrettyTable()
    output_table.field_names = ("id", "rom_amount", "vm_id")
    output_table.align = "l"
    for hd_obj in hd_objs:
        rows = (hd_obj.id, hd_obj.rom_amount, hd_obj.vm_id)
        output_table.add_row(rows)
    print(output_table)
