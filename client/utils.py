import json
import random

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_data_vm() -> str:
    """Random data for vm."""
    data = {
        "ram_amount": random.randint(500, 10000),
        "cpu_amount": random.randint(1, 14),
        "hd": [
            {"rom_amount": random.randint(500, 10000)}
            for _ in range(random.randint(1, 5))
        ],
    }
    data = json.dumps(data)
    return data


def get_password_hash(password: str) -> str:
    """Make hashed password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare between str pass and hashed pass."""
    return pwd_context.verify(plain_password, hashed_password)
