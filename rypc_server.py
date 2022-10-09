import rpyc
import sys
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Cipher import DES
from secrets import token_bytes

_key_des__ = token_bytes(8)
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

# generate key
def generate_key(password):
    __key_aes__ = hashlib.sha256(password.encode()).digest()


def encrypt_DES(msg):
    cipher = DES.new(_key_des__, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, ciphertext, tag


def decrypt_DES(nonce, ciphertext, tag):
    cipher = DES.new(_key_des__, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False


class SscretMessageService(rpyc.Service):
    def exposed_encrypt_AES(self, plain_text, file_path, password):
       generate_key(password)
       ciphertext = encrypt_AES(plain_text)
       with open(file_path, 'wb') as f:
            f.write(ciphertext)
       print("File encrypted [server]")
    def exposed_decrypt_AES(self, cipher_text, file_path, password):
        __key__ = password
        cipher_text = cipher_text.decode('utf-8')
        plaintext = decrypt_AES(cipher_text)
        with open(file_path, 'w') as f:
            f.write(plaintext)
        print("File decrypted [server]")
    def exposed_encrypt_DES(self, plain_text, file_path):
        nonce, ciphertext, tag = encrypt_DES(plain_text)
        with open(file_path, 'wb') as f:
            f.write(nonce)
            f.write(ciphertext)
            f.write(tag)
        print("File encrypted [server]")
    def exposed_decrypt_DES(self, cipher_text, file_path):
        nonce = cipher_text[:8]
        ciphertext = cipher_text[8:-16]
        tag = cipher_text[-16:]
        plaintext = decrypt_DES(nonce, ciphertext, tag)
        with open(file_path, 'w') as f:
            f.write(plaintext)
        print("File decrypted [server]")
    def exposed_quit(self, function):
        print('Shutting down...')
        function("Bye bye")
        sys.exit(0)



def main():
    from rpyc.utils.server import OneShotServer
    t = OneShotServer(SscretMessageService, port = 18861)
    t.start()
    t.close()
    sys.exit(0)

if __name__ == '__main__':
    main()