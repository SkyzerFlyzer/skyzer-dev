import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class Encryption:

    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, text):
        text = self._pad(text)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(text.encode())).decode('utf-8')

    def decrypt(self, text):
        text = base64.b64decode(text)
        iv = text[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return Encryption._un_pad(cipher.decrypt(text[AES.block_size:])).decode('utf-8')

    def _pad(self, raw_string):
        return (raw_string + (self.block_size - len(raw_string) % self.block_size) *
                chr(self.block_size - len(raw_string) % self.block_size))

    @staticmethod
    def _un_pad(s):
        return s[:-ord(s[len(s) - 1:])]
