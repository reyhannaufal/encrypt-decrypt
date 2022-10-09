import rpyc
import time
from enum import Enum

class Command(Enum):
    E_AES  = "encrypt_aes"
    D_AES = "decrypt_aes"
    E_DES = "encrypt_des"
    D_DES = "decrypt_des"
    QUIT = "quit"
    
class TEXT_INPUT(Enum):
    PLAINTEXT = "Input path file (Plaintext): "
    CIPHERTEXT = "Input path file (Ciphertext): "
    PASSWORD = "Input password: "
    SUCESS = "Sucess!"

def print_menu():
    print(f'{"="*20} Menu {"="*20}')
    print(f'./example.txt')
    for i in Command:
        print(f'{i.value}')
    print(f'{"="*20} {"="*20}')

def user_input_handler(proxy, user_input_command):
    print(
            f"Command: {user_input_command} - {Command(user_input_command).value}")
    if(user_input_command == Command.E_AES.value):
        file_path = input(TEXT_INPUT.PLAINTEXT.value)
        password = input(TEXT_INPUT.PASSWORD.value)
        with open(file_path, 'r') as f:
            data_file = f.read()
        proxy.root.encrypt_AES(data_file, file_path, password)
        print(TEXT_INPUT.SUCESS.value)
    elif(user_input_command == Command.D_AES.value):
        file_path = input(TEXT_INPUT.CIPHERTEXT.value)
        password = input(TEXT_INPUT.PASSWORD.value)
        with open(file_path, 'rb') as f:
            data_file = f.read()
        proxy.root.decrypt_AES(data_file, file_path, password)
        print(TEXT_INPUT.SUCESS.value)
    elif(user_input_command == Command.E_DES.value):
        file_path = input(TEXT_INPUT.PLAINTEXT.value)
        with open(file_path, 'r') as f:
            data_file = f.read()
        proxy.root.encrypt_DES(data_file, file_path)
        print(TEXT_INPUT.SUCESS.value)
    elif(user_input_command == Command.D_DES.value):
        file_path = input(TEXT_INPUT.CIPHERTEXT.value)
        with open(file_path, 'rb') as f:
            data_file = f.read()
        proxy.root.decrypt_DES(data_file, file_path)
        print(TEXT_INPUT.SUCESS.value)
    elif(user_input_command == Command.QUIT.value):
        time.sleep(2)
        proxy.close()

def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    option = " "
    while(option != Command.QUIT.value):
        print_menu()
        option = input("Input command: ")
        msg = option.split()
        user_input_command = msg[0]
        if user_input_command not in Command._value2member_map_: 
            print("No Command, please retry\n==========================\n")
            continue
        user_input_handler(proxy, user_input_command)


if __name__ == '__main__':
    main()