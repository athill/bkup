# sudo pip install pycrypto

## from http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
## looking into password protecting files
import os

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

class FileCrypt:

    def derive_key_and_iv(self, password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = self.derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def decrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = self.derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)

## usage

tmpdir= os.path.join(os.path.expanduser('~'), 'tmp');
in_filename = os.path.join(tmpdir, 'home.tgz')
out_filename = os.path.join(tmpdir, 'home.tgz.ec')
password='foo'
hashed = md5(password).hexdigest()

fc = FileCrypt()
with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
    fc.encrypt(in_file, out_file, password)

with open(out_filename, 'rb') as in_file, open(in_filename, 'wb') as out_file:
    fc.decrypt(in_file, out_file, password)            