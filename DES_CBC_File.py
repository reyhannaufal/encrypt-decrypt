from fileinput import filename
import os
from tarfile import BLOCKSIZE
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES


def getKey(keySize):
    key = os.urandom(keySize)
    return key


def getIV(blockSize):
    iv = os.urandom(blockSize)
    return iv


def encrypt_image(filename, key, iv):
    BLOCKSIZE = 16
    encrypted_filename = "encrypted_" + filename

    with open(filename, "rb") as file1:
        data = file1.read()

        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, BLOCKSIZE))

        with open(encrypted_filename, "wb") as file2:
            file2.write(ciphertext)

    return encrypted_filename


def decrypt_image(filename, key, iv):
    BLOCKSIZE = 16
    decrypted_filename = "decrypted_" + filename

    with open(filename, "rb") as file1:
        data = file1.read()

        cipher2 = DES.new(key, DES.MODE_CBC, iv)
        decrypted_data = unpad(cipher2.decrypt(data), BLOCKSIZE)

        with open(decrypted_filename, "wb") as file2:
            file2.write(decrypted_data)

    return decrypted_filename


KEYSIZE = 8
BLOCKSIZE = 8
filename = "message.txt"

key = getKey(KEYSIZE)
iv = getIV(BLOCKSIZE)

encrypted_filename = encrypt_image(filename, key, iv)
decrypted_filename = decrypt_image(encrypted_filename, key, iv)
