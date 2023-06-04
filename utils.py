from cryptography.fernet import Fernet
from subprocess import check_output
from loguru import logger

random_string_command = "openssl rand -base64 256"


def generate_token() -> str:
    token = check_output(random_string_command, shell=True, executable='/bin/bash').decode().replace("\n", "")
    return token


def generate_crypt_key() -> str:
    key = Fernet.generate_key().decode()
    return key


def decrypt_data(crypt_key: str, encrypted_data: str) -> str:
    fernet = Fernet(crypt_key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()

