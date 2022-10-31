# - Create an application that takes a PDF document and the user’s private key to sign the document digitally.
# - The application should then verify the signature using the public key.

# Importing the required libraries
import PyPDF2
import os
import sys
import base64
import hashlib
import binascii
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# Function to sign the PDF document
def sign_pdf(pdf_file, private_key):
    # Reading the PDF file
    pdf = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    pdf_writer = PyPDF2.PdfFileWriter()

    # Adding the pages to the PDF writer
    for page in range(pdf_reader.numPages):
        pdf_writer.addPage(pdf_reader.getPage(page))

    # Getting the signature
    signature = get_signature(private_key)

    # Adding the signature to the PDF writer
    # pdf_writer.addSignature(signature, None, None, None, None)

    # Creating a new file to save the signed PDF
    signed_pdf = open('signed_' + pdf_file, 'wb')
    pdf_writer.write(signed_pdf)

    # Closing the files
    signed_pdf.close()
    pdf.close()

# Function to get the signature
def get_signature(private_key):
    # Reading the private key
    with open(private_key, 'rb') as f:
        key = f.read()
        f.close()

    # Creating the signature
    signature = PyPDF2.generic.DictionaryObject()
    # signature.update({
    #     # PyPDF2.generic.NameObject('/Type'): PyPDF2.generic.NameObject('/Sig'),
    #     # PyPDF2.generic.NameObject('/Filter'): PyPDF2.generic.NameObject('/Adobe.PPKLite'),
    #     # PyPDF2.generic.NameObject('/SubFilter'): PyPDF2.generic.NameObject('/adbe.pkcs7.detached'),
    #     PyPDF2.generic.NameObject('/Contents'): PyPDF2.generic.ByteStringObject(get_signature_contents(key)),
    # })
    return signature

# Function to get the signature contents
def get_signature_contents(private_key):
    # Reading the private key
    with open(private_key, 'rb') as f:
        key = f.read()
        f.close()

    # Creating the signature contents
    private_key = RSA.importKey(key)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(b'Hello World')
    sign = signer.sign(digest)
    return sign

# Function to verify the signature
def verify_signature(pdf_file, public_key):
    # Reading the PDF file
    pdf = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)

    # Getting the signature
    signature = pdf_reader.getSignature(0)

    # Verifying the signature
    if signature:
        if verify_signature_contents(signature, public_key):
            print('The signature is valid.')
        else:
            print('The signature is invalid.')
    else:
        print('The PDF is not signed.')

    # Closing the file
    pdf.close()

# Function to verify the signature contents
def verify_signature_contents(signature, public_key):
    # Reading the public key
    with open(public_key, 'rb') as f:
        key = f.read()
        f.close()

    # Verifying the signature contents
    public_key = RSA.importKey(key)
    signer = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(b'Hello World')
    if signer.verify(digest, signature['/Contents']):
        return True
    return False

# Main function
def main():
    # Getting the PDF file name
    pdf_file = input('Enter the PDF file name: ')

    # Getting the private key file name
    private_key = input('Enter the private key file name: ')

    # Getting the public key file name
    public_key = input('Enter the public key file name: ')

    # Signing the PDF document
    sign_pdf(pdf_file, private_key)

    # Verifying the signature
    verify_signature('signed_' + pdf_file, public_key)

# Calling the main function
if __name__ == '__main__':
    main()
    