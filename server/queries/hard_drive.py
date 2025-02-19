CREATE_HD = """\
INSERT INTO hard_drives (vm_id, rom_amount)
VALUES ($1, $2)
RETURNING *;
"""
UPDATE_HD = """\
UPDATE hard_drives
SET vm_id = $1, rom_amount = $2
WHERE id = $3;
"""
SET_NULL_HD_VM_ID = """\
UPDATE hard_drives
SET vm_id = null
WHERE vm_id = $1;
"""
DELETE_HD = """\
DELETE FROM hard_drives
WHERE id = $1;
"""

GET_ALL_HD = """\
SELECT * FROM hard_drives
"""

GET_ALL_HD_FOR_VM = """\
SELECT id, rom_amount FROM hard_drives
WHERE vm_id = $1
"""

GET_HD_FOR_KEY = """\
SELECT * FROM hard_drives
WHERE {} = $1
"""
