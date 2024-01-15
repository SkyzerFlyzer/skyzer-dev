import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class Encryption:

    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, text: str) -> str:
        text = self._pad(text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(text.encode())
        encrypted_text = ciphertext.decode()
        return iv.decode() + encrypted_text

    def decrypt(self, text: str) -> str:
        text = text.encode()
        iv = text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(text[self.block_size:])
        return self._un_pad(plaintext.decode())

    def _pad(self, raw_string: str) -> str:
        return (raw_string + (self.block_size - len(raw_string) % self.block_size) *
                chr(self.block_size - len(raw_string) % self.block_size))

    @staticmethod
    def _un_pad(s: str) -> str:
        return s[:-ord(s[len(s) - 1:])]
