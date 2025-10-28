from Crypto.Cipher import AES
from base64 import b64encode, b64decode


load_dotenv()  # Læs .env i root
SECRET_KEY = os.getenv("SECRET_KEY").encode()  # AES-key som bytes


#  I et rigtigt system skal denne nøgle ligge sikkert i en .env-fil!
SECRET_KEY = b"1234567890123456"  # præcis 16 bytes (AES-128)

def encrypt_value(value: str) -> str:
    """Krypter tekstværdi og returner Base64-streng"""
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(value.encode("utf-8"))
    return b64encode(cipher.nonce + ciphertext).decode("utf-8")

def decrypt_value(encoded: str) -> str:
    """Dekrypter Base64-streng og returner original tekst"""
    raw = b64decode(encoded)
    nonce, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode("utf-8")