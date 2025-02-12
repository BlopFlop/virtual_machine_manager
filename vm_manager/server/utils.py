from uuid import uuid4


def generate_token() -> str:
    return str(uuid4())
