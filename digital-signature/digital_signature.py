import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

def sign_file(filename, private_key):
    h = SHA256.new()
    signed_file = 'signed_'+filename

    with open(filename, 'rb') as f:
        with open(signed_file, 'xb') as fw:
            fw.write(f.read())
        h.update(f.read())
    signer = PKCS1_v1_5.new(private_key)

    signature = signer.sign(h)

    # Sign PDF file
    with open(signed_file, 'r+b') as f:
        f.seek(0, 2)
        f.write(signature)

    return signature

def verify_file(filename, signature, public_key):
    h = SHA256.new()
    print(filename)
    with open(filename, 'rb') as f:
        h.update(f.read())
    verifier = PKCS1_v1_5.new(public_key)

    # Verify Signed PDF file
    with open(filename, 'r+b') as f:
        f.seek(0, 2)
        try:
            verifier.verify(h, signature)
            return "The signature is valid."
        except (ValueError, TypeError):
            return "The signature is NOT valid."

def main():
    if len(sys.argv) != 4:
        print('Usage: digital_signature.py <private_key> <public_key> <filename>')
        return
    private_key = RSA.importKey(open(sys.argv[1]).read())
    public_key = RSA.importKey(open(sys.argv[2]).read())
    filename = sys.argv[3]
    signature = sign_file(filename, private_key)
    print('Signature: {}'.format(signature))
    print('Verified: {}'.format(verify_file('signed_'+filename, signature, public_key)))

if __name__ == '__main__':
    main()

