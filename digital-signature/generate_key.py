from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) 

publickey = key.publickey()
print(publickey.exportKey())

def generate_key():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator) 
    publickey = key.publickey()
    return key, publickey

def save_key(key, filename):
    if not filename.endswith('.pem'):
        filename += '.pem'
    with open(filename, 'wb') as f:
        f.write(key.exportKey())

def load_key(filename):
    if not filename.endswith('.pem'):
        filename += '.pem'
    with open(filename, 'rb') as f:
        return RSA.importKey(f.read())

def main():
    private_key_file = input('Enter filename to save private key: ')
    key, publickey = generate_key()
    save_key(key, private_key_file)
    public_key_file = input('Enter filename to save public key: ')
    save_key(publickey, public_key_file)

if __name__ == '__main__':
    main()



