from cryptography.fernet import Fernet

# Generer en korrekt Fernet nøgle
fernet_key = Fernet.generate_key()
print(f"ENCRYPTION_KEY={fernet_key.decode()}")

from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())