import rpyc
import sys
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt_AES(raw):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=__key__)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt_AES(enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(mode= AES.MODE_CFB,iv= iv, key=__key__)
    return base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8').rstrip(chr(AES.block_size))

# generate key
def generate_key(password):
    global __key__
    __key__ = hashlib.sha256(password.encode()).digest()


class SscretMessageService(rpyc.Service):
    def exposed_encrypt_AES(self, plain_text, file_path, password):
       generate_key(password)
       ciphertext = encrypt_AES(plain_text)
       with open(file_path, 'wb') as f:
            f.write(ciphertext)
       print(__key__)
       print("File encrypted [server]")
    def exposed_decrypt_AES(self, cipher_text, file_path, password):
        __key__ = password
        cipher_text = cipher_text.decode('utf-8')
        plaintext = decrypt_AES(cipher_text)
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