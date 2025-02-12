from typing import Final

CREATE_VM: Final[
    str
] = """\
INSERT INTO virtual_machines (ram_amount, cpu_amount, token)
VALUES ($1, $2, $3)
"""
UPDATE_VM: Final[
    str
] = """\
UPDATE virtual_machines
SET ram_amount = $1, cpu_amount = $2, token = $3
WHERE id = $4;
"""
DELETE_VM: Final[
    str
] = """\
DELETE FROM virtual_machines
WHERE id = $1;
"""

CREATE_HD: Final[
    str
] = """\
INSERT INTO hard_drives (vm_id, rom_amount)
VALUES ($1, $2)
"""
UPDATE_HD: Final[
    str
] = """\
UPDATE hard_drives
SET vm_id = $1, rom_amount = $2
WHERE id = $3;
"""
DELETE_HD: Final[
    str
] = """\
DELETE FROM hard_drives
WHERE id = $1;
"""

GET_ALL_HD: Final[
    str
] = """\
SELECT * FROM hard_drives
"""

GET_ALL_HD_FOR_VM: Final[
    str
] = """\
SELECT id, rom_amount FROM hard_drives
WHERE vm_id = $1
"""

GET_VM_FOR_KEY: Final[
    str
] = """\
SELECT * FROM virtual_machines
WHERE $1 = $2
"""

GET_HD_FOR_KEY: Final[
    str
] = """\
SELECT * FROM hard_drives
WHERE $1 = $2
"""

GET_VM_FOR_TOKEN: Final[
    str
] = """\
SELECT * FROM virtual_machines
WHERE auth_token = $1
"""

GET_ONLINE_VM: Final[
    str
] = """\
SELECT * FROM virtual_machines
WHERE is_online
"""

GET_AUTH_VM: Final[
    str
] = """\
SELECT * FROM virtual_machines
WHERE token IS NOT null
"""
GET_ALL_VM: Final[
    str
] = """\
SELECT * FROM virtual_machines
"""
