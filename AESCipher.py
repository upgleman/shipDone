import base64
from Crypto.Cipher import AES

BS = 16
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s) - 1:])])


class AESCipher(object):
    def __init__(self, key):
        self.key = key.encode('utf8')

    def encrypt(self, message):
        message = message.encode('utf8')
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv())
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv())
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def __iv(self):
        return self.key[0:16]