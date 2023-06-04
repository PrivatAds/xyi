from config import CRYPT_KEY, TOKEN
from random import choices
from string import ascii_uppercase
from cryptography.fernet import Fernet

fernet = Fernet(CRYPT_KEY)

def generate_random_code() -> str:
    code = "".join(choices(ascii_uppercase, k=6))
    return code


def decrypt_data(encrypted_data: str) -> str:
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data


def validate_token(token: str) -> bool:
    return token == TOKEN
