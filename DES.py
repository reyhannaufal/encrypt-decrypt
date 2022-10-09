from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

key = pad(b"mykey", DES.block_size)
iv = pad(b"myiv", DES.block_size)


def encrypt(plaintext):
    data_bytes = bytes(plaintext, 'utf-8')
    padded_bytes = pad(data_bytes, DES.block_size)
    DES_obj = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = DES_obj.encrypt(padded_bytes)
    return ciphertext


def decrypt(ciphertext):
    DES_obj = DES.new(key, DES.MODE_CBC, iv)
    raw_bytes = DES_obj.decrypt(ciphertext)
    extracted_bytes = unpad(raw_bytes, DES.block_size)
    return extracted_bytes


ciphertext = encrypt(input('Enter a message: '))
plaintext = decrypt(ciphertext)

print(f'Cipher Text: {binascii.hexlify(ciphertext)}')

if not plaintext:
    print('Message is corrupted!')
else:
    print(f'Plain Text: {plaintext}')
