import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

def sign_file(filename, private_key):
    h = SHA256.new()
    with open(filename, 'rb') as f:
        h.update(f.read())
    signer = PKCS1_v1_5.new(private_key)
    return signer.sign(h)

def verify_file(filename, signature, public_key):
    h = SHA256.new()
    with open(filename, 'rb') as f:
        h.update(f.read())
    verifier = PKCS1_v1_5.new(public_key)
    return verifier.verify(h, signature)

def main():
    if len(sys.argv) != 4:
        print('Usage: digital_signature.py <private_key> <public_key> <filename>')
        return
    private_key = RSA.importKey(open(sys.argv[1]).read())
    public_key = RSA.importKey(open(sys.argv[2]).read())
    filename = sys.argv[3]
    signature = sign_file(filename, private_key)
    print('Signature: {}'.format(signature))
    print('Verified: {}'.format(verify_file(filename, signature, public_key)))

if __name__ == '__main__':
    main()

