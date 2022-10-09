import rpyc
import time
from enum import Enum

class Command(Enum):
    E_AES  = "encrypt_aes"
    D_AES = "decrypt_aes"
    E_DES = "encrypt_des"
    D_DES = "decrypt_des"
    QUIT = "quit"

def print_menu():
    print(f'{"="*20} Menu {"="*20}')
    for i in Command:
        print(f'{i.value}')
    print(f'{"="*20} {"="*20}')

def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    option = " "
    while(option != "quit"):
        print_menu()
        option=input("Input command: ")
        msg=option.split()
        user_input_command = msg[0]
        print(
            f"Command: {user_input_command} - {Command(user_input_command).value}")
        if(user_input_command == Command.E_AES.value):
            file_path = input("input path file [plaintext]: ")
            password = input("input password: ")
            with open(file_path, 'r') as f:
                data_file = f.read()
            proxy.root.encrypt_AES(data_file, file_path, password)
            print("File berhasil diencrypt")
        elif(user_input_command == Command.D_AES.value):
            file_path = input("input path file [ciphertext]: ")
            password = input("input password: ")
            with open(file_path, 'rb') as f:
                data_file = f.read()
            proxy.root.decrypt_AES(data_file, file_path, password)
            print("File berhasil diencrypt")
        elif(user_input_command == Command.E_DES.value):
            file_path = input("input path file [plaintext]: ")
            with open(file_path, 'r') as f:
                data_file = f.read()
            proxy.root.encrypt_DES(data_file, file_path)
            print("File berhasil diencrypt")
        elif(user_input_command == Command.D_DES.value):
            file_path = input("input path file [ciphertext]: ")
            with open(file_path, 'rb') as f:
                data_file = f.read()
            proxy.root.decrypt_DES(data_file, file_path)
            print("File berhasil diencrypt")
        elif(user_input_command == Command.QUIT.value):
            time.sleep(2)
            proxy.close()
        else:
            print("No Command, please retry\n==========================\n")
if __name__ == '__main__':
    main()