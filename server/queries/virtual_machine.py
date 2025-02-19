CREATE_VM = """\
INSERT INTO virtual_machines (ram_amount, cpu_amount)
VALUES ($1::int, $2::int)
RETURNING *;
"""
UPDATE_VM = """\
UPDATE virtual_machines
SET ram_amount = $1,
    cpu_amount = $2,
    is_online = $3,
    is_auth = $4
WHERE id = $5;
"""
DELETE_VM = """\
DELETE FROM virtual_machines
WHERE id = $1;
"""

GET_VM_FOR_KEY = """\
SELECT * FROM virtual_machines
WHERE {} = $1
"""

GET_ALL_VM = """\
SELECT * FROM virtual_machines
"""
