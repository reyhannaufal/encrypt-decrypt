import rpyc
import sys
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

__key_des__ = pad(b"mykey", DES.block_size)
__iv_des__ = pad(b"myiv", DES.block_size)
__key_aes__ = None


def encrypt_AES(raw):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=__key_aes__)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt_AES(enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=__key_aes__)
    return base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8').rstrip(chr(AES.block_size))

def generate_key(password):
    __key_aes__ = hashlib.sha256(password.encode()).digest()


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
       generate_key(password)
       ciphertext = encrypt_AES(plain_text)
       with open(file_path, 'wb') as f:
            f.write(ciphertext)
    def exposed_decrypt_AES(self, cipher_text, file_path, password):
        __key__ = password
        cipher_text = cipher_text.decode('utf-8')
        plaintext = decrypt_AES(cipher_text)
        with open(file_path, 'w') as f:
            f.write(plaintext)
    def exposed_encrypt_DES(self, plain_text, file_path):
        ciphertext = encrypt_DES(plain_text)
        result = binascii.hexlify(ciphertext)
        with open(file_path, 'wb') as f:
            f.write(result)
    def exposed_decrypt_DES(self, cipher_text, file_path):
        plaintext = decrypt_DES(binascii.unhexlify(cipher_text))
        if not plaintext:
            print('Message is corrupted!')
        else:
            with open(file_path, 'w') as f:
                f.write(plaintext.decode("utf-8"))
    def exposed_encrypt_RC4(self, plain_text, file_path, password):
       ciphertext = encrypt_RC4(plain_text, password)
       with open(file_path, 'w') as f:
            f.write(ciphertext)
    def exposed_decrypt_RC4(self, cipher_text, file_path, password):
       plaintext = decrypt_RC4(cipher_text, password)
       with open(file_path, 'w') as f:
            f.write(plaintext)
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