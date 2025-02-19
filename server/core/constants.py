from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "vm_manager.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

MG_SCRIPT: Final[Path] = BASE_DIR / r"migrations/init.sql"

ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra/.env"

CLEAN_CONSOLE: Final[str] = "\r\033[K"

# commands
AUTH: Final[str] = "/auth"
LOGOUT: Final[str] = "/logout"

VM_ONLINE: Final[str] = "/vm_online"
VM_AUTH: Final[str] = "/vm_auth"
VM_ALL: Final[str] = "/vm"

HD_LIST: Final[str] = "/hd"

HELP: Final[str] = "/help"
CLIENTS: Final[str] = "/clients"
MESSAGE: Final[str] = "/msg"

# output
HELP_MSG: Final[
    str
] = """\

Доступные команды:
- /auth <адрес_клиента> <пароль> - Аутентифицировать клиента.
   Пример: /auth 127.0.0.1:8001 mypassword
- /logout <адрес_клиента> - Выйти из авторизованной виртуальной машины.
   Пример: /logout 127.0.0.1:8001
- /msg <адрес_клиента> <Сообщение> - Послать сообщение.
   Пример: /auth 127.0.0.1:8001 Привет
- /vm_online - Вывести список всех подключенных виртуальных машин с их
   параметрами. Пример: /vm online
- /vm_auth - Вывести список всех авторизованных виртуальных машин с их
   параметрами. Пример: /vm auth
- /vm - Вывести список всех виртуальных машин, которые когда-либо
   подключались. Пример: /vm
- /hd - Вывести список всех жестких дисков с их параметрами
    (включая привязку к ВМ). Пример: /hd
- /clients - Вывод всех подключенных клиентов.
"""
