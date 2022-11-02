import shutil
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Signature import pss

def sign_file(filename, private_key):
    h = SHA256.new()
    signed_file = 'signed_'+filename

    with open(filename, 'rb') as f:
        h.update(f.read())
    signer = pss.new(private_key)
    signature = signer.sign(h)

    # Sign PDF file
    with open(signed_file, 'wb') as f:
        with open(filename, 'rb') as fb:
            f.write(fb.read())
        f.write(signature)
    return signature

def verify_file(filename, public_key):
    h = SHA256.new()
    s = b''
    with open(filename, 'r+b') as f:
        # Take signature at the end of file
        f.seek(-128, 2)
        s = f.read()
    print(s)
    
    with open(filename, 'r+b') as f:
        with open('___dummy.pdf', 'w+b') as fb:
            shutil.copyfileobj(f, fb)
            fb.seek(-128, 2)
            fb.truncate()
            # Read only the original file part
            fb.seek(0, 0)
            h.update(fb.read())
    os.remove('___dummy.pdf')

    # Verify Signed PDF file
    mess=''
    try:
        pss.new(public_key).verify(h, s)
        mess="The signature is valid."
    except (ValueError, TypeError):
        mess="The signature is NOT valid."
    return mess

def main():
    if len(sys.argv) != 4 :
        print('Usage: digital_signature.py <sign/verify> <private_key/public_key> <filename/signed_filename>')
        return
    key = RSA.importKey(open(sys.argv[2]).read())
    filename = sys.argv[3]
    if sys.argv[1] == 'sign':
        signature = sign_file(filename, key)
        print('Signature: {}'.format(signature))
    elif sys.argv[1] == 'verify':
        print('Verified: {}'.format(verify_file(filename, key)))
    else:
        print('Usage: digital_signature.py <sign/verify> <private_key/public_key> <filename>')

if __name__ == '__main__':
    main()