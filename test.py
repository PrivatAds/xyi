from cryptography.fernet import Fernet
from config import CRYPT_KEY

fernet = Fernet(CRYPT_KEY)

string = "<h1>World<h1>"

encrypted = fernet.encrypt(string.encode())

print(encrypted)
