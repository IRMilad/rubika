import re
import json
import base64
import string
import secrets
from json import JSONDecoder
from Crypto.Cipher import AES


class Crypto(object):
    AES_IV = b'\x00' * 16

    @classmethod
    def passphrase(cls, auth):
        # zabcdefgjklmnopqhirstuvwxsfegsvr to qrabcdefijklmnopgbonpbeastuvwxyz
        if len(auth) != 32:
            raise ValueError('auth length should be 32 digits')

        result = ''
        chunks = re.findall(r'\S{8}', auth)
        for character in (chunks[2] + chunks[0] + chunks[3] + chunks[1]):
            result += chr(((ord(character) - 97 + 9) % 26) + 97)
        return result

    @classmethod
    def secret(cls, length):
        return ''.join(secrets.choice(string.ascii_lowercase)
                       for _ in range(length))

    @classmethod
    def decrypt(cls, data, key):
        decoder = JSONDecoder()
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        result, _ = decoder.raw_decode(cipher.decrypt(
            base64.b64decode(data)).decode('utf-8'))
        return result

    @classmethod
    def encrypt(cls, data, key):
        if not isinstance(data, str):
            data = json.dumps(data, default=lambda x: str(x))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return (
            base64.b64encode(cipher.encrypt(data.encode('utf-8')))
            .decode('utf-8')
        )
