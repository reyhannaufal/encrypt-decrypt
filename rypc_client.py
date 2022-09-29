import rpyc
import time

def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    option = " "
    while(option != "quit"):
        option=input("Input command: ")
        msg=option.split()
        if(msg[0] == "e_aes"):
            file_path = input("input path file [plaintext]: ")
            password = input("input password: ")
            with open(file_path, 'r') as f:
                data_file = f.read()
            proxy.root.encrypt_AES(data_file, file_path, password)
            print("File berhasil diencrypt")
        elif(msg[0] == "d_aes"):
            file_path = input("input path file [ciphertext]: ")
            password = input("input password: ")
            with open(file_path, 'rb') as f:
                data_file = f.read()
            proxy.root.decrypt_AES(data_file, file_path, password)
            print("File berhasil diencrypt")
        elif(msg[0] == "quit"):
            time.sleep(2)
            proxy.close()
        else:
            print("No Command, please retry\n==========================\n")
if __name__ == '__main__':
    main()