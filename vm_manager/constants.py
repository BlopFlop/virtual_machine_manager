from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "vm_manager.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR / r"infra/.env"

MIGRATE_SQL: Final[str] = """\
CREATE TABLE virtual_machines (
    id SERIAL PRIMARY KEY,
    ram_amount BIGINT NOT NULL,
    cpu_amount INT NOT NULL,
    token UUID UNIQUE,
    is_online BOOLEAN DEFAULT FALSE
);

CREATE TABLE hard_drives (
    id SERIAL PRIMARY KEY,
    vm_id INT REFERENCES virtual_machines(id),
    rom_amount BIGINT NOT NULL
);
"""
