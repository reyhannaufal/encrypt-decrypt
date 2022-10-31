# generate public and private key and export to file

from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key

publickey = key.publickey() # pub key export for exchange
print(publickey.exportKey())

f = open('private.pem','wb')
f.write(key.exportKey('PEM'))
f.close()

f = open('public.pem','wb')
f.write(publickey.exportKey('PEM'))
f.close()


    