from pydoc import plain
import rpyc
import sys
import base64
import hashlib
import os
import pyAesCrypt

from timer import Timer
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad


__key_des__ = pad(b"mykey", DES.block_size)
__iv_des__ = pad(b"myiv", DES.block_size)
SPECIAL_KEY_FOR_FILES = 'why_so_serious'


RunningTime = Timer()


def encrypt_AES(raw, key):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=key)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt_AES(enc, key):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=key)
    return base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8').rstrip(chr(AES.block_size))

def encrypt_file_AES(file_name):
    output = file_name + ".enc"
    pyAesCrypt.encryptFile(file_name, output, SPECIAL_KEY_FOR_FILES)
    return output

def decrypt_file_AES(file_name):
    dfile = file_name.split(".")
    output = dfile[0] + "dec." + dfile[1]
    pyAesCrypt.decryptFile(file_name, output, SPECIAL_KEY_FOR_FILES)
    return

def generate_key(password):
    __key_aes__ = hashlib.sha256(password.encode()).digest()
    return __key_aes__


def encrypt_DES(plaintext):
    data_bytes = bytes(plaintext, 'utf-8')
    padded_bytes = pad(data_bytes, DES.block_size)
    DES_obj = DES.new(__key_des__, DES.MODE_CBC, __iv_des__)
    ciphertext = DES_obj.encrypt(padded_bytes)
    return ciphertext


def decrypt_DES(ciphertext):
    DES_obj = DES.new(__key_des__, DES.MODE_CBC, __iv_des__)
    raw_bytes = DES_obj.decrypt(ciphertext)
    extracted_bytes = unpad(raw_bytes, DES.block_size)
    return extracted_bytes

def encrypt_DES_files(filename, key, iv):
    BLOCKSIZE = 16
    encrypted_filename = "encrypted_" + filename

    with open(filename, "rb") as file1:
        data = file1.read()

        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, BLOCKSIZE))

        with open(encrypted_filename, "wb") as file2:
            file2.write(ciphertext)

    return encrypted_filename


def decrypt_DES_files(filename, key, iv):
    BLOCKSIZE = 16
    decrypted_filename = "decrypted_" + filename

    with open(filename, "rb") as file1:
        data = file1.read()

        cipher2 = DES.new(key, DES.MODE_CBC, iv)
        decrypted_data = unpad(cipher2.decrypt(data), BLOCKSIZE)

        with open(decrypted_filename, "wb") as file2:
            file2.write(decrypted_data)

    return decrypted_filename

def getKey(keySize):
    key = os.urandom(keySize)
    return key


def getIV(blockSize):
    iv = os.urandom(blockSize)
    return iv

def KSA(key):
    sched = [i for i in range(0, 256)]
    
    i = 0
    for j in range(0, 256):
        i = (i + sched[j] + key[j % len(key)]) % 256
        
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
        
    return sched
    

def stream_generation(sched):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (sched[i] + j) % 256
        
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
        
        yield sched[(sched[i] + sched[j]) % 256]        


def encrypt_RC4(text, key):
    text = [ord(char) for char in text]
    key = [ord(char) for char in key]
    
    sched = KSA(key)
    key_stream = stream_generation(sched)
    
    ciphertext = ''
    for char in text:
        enc = str(hex(char ^ next(key_stream))).upper()
        ciphertext += (enc)
        
    return ciphertext

def decrypt_RC4(ciphertext, key):
    ciphertext = ciphertext.split('0X')[1:]
    ciphertext = [int('0x' + c.lower(), 0) for c in ciphertext]
    key = [ord(char) for char in key]
    
    sched = KSA(key)
    key_stream = stream_generation(sched)
    
    plaintext = ''
    for char in ciphertext:
        dec = str(chr(char ^ next(key_stream)))
        plaintext += dec
    
    return plaintext


class SecretMessageService(rpyc.Service):
    def exposed_encrypt_AES(self, plain_text, file_path, password):
        RunningTime.start()
        key = generate_key(password)
        ciphertext = None
        if file_path.endswith('.mp4') or file_path.endswith('.jpg'):
            ciphertext = encrypt_file_AES(file_path)
        else:
            ciphertext = encrypt_AES(plain_text, key)
            with open(file_path, 'wb') as f:
                    f.write(ciphertext)
        print("==========================================================")
        print("Running Time - Encrypt AES Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_decrypt_AES(self, cipher_text, file_path, password):
        key = generate_key(password)
        RunningTime.start()
        if file_path.endswith('.enc'):
            plaintext = decrypt_file_AES(file_path)
        else:
            plaintext = decrypt_AES(cipher_text, key)
            with open(file_path, 'w') as f:
                f.write(plaintext)
        print("==========================================================")
        print("Running Time - Decrypt AES Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_encrypt_DES(self, plain_text, file_path):
        RunningTime.start()
        global key_des_new
        key_des_new = getKey(8)
        global iv_des_new
        iv_des_new = getIV(8)
        encrypt_DES_files(file_path, key_des_new, iv_des_new)
        print("==========================================================")
        print("Running Time - Encrypt DES Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_decrypt_DES(self, cipher_text, file_path):
        RunningTime.start()
        decrypt_DES_files(file_path, key_des_new, iv_des_new)
        print("==========================================================")
        print("Running Time - Decrypt DES Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_encrypt_RC4(self, plain_text, file_path, password):
        RunningTime.start()
        if file_path.endswith('.mp4') or file_path.endswith('.jpg') or file_path.endswith('.png'):
            output = file_path + ".enc"
            text = plain_text.decode('utf-8')
            ciphertext = encrypt_RC4(text, password)
            with open(output, 'w') as f:
                f.write(ciphertext)
        else:
            ciphertext = encrypt_RC4(plain_text, password)
            with open(file_path, 'w') as f:
                f.write(ciphertext)
        print("==========================================================")
        print("Running Time - Encrypt RC4 Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_decrypt_RC4(self, cipher_text, file_path, password):
        RunningTime.start()
        if file_path.endswith('.enc'):
            dfile = file_path.split(".")
            output = "." + dfile[0] + dfile[1] + "dec."+ dfile[2]
            plaintext = decrypt_RC4(cipher_text, password)
            with open(output, 'wb') as f:       
                f.write(base64.b64decode((plaintext)))

        else:
            plaintext = decrypt_RC4(cipher_text, password)
            with open(file_path, 'w') as f:
                f.write(plaintext)
        print("==========================================================")
        print("Running Time - Decrypt RC4 Method")
        RunningTime.stop()
        print("==========================================================")
    def exposed_quit(self, function):
        print('Shutting down...')
        function("Bye bye")
        sys.exit(0)



def main():
    from rpyc.utils.server import OneShotServer
    t = OneShotServer(SecretMessageService, port = 18861)
    t.start()
    t.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
