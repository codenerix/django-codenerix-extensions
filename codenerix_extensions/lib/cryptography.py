import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    """
    Adapted solution from: https://stackoverflow.com/a/21928790/1481040
    """

    def __init__(self):
        self.bs = 32

    def encrypt(self, raw, key):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        hashkey = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        hashkey = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
