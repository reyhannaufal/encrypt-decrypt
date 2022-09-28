import rpyc
import time

def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    option = " "
    while(option != "quit"):
        option=input("Input command: ")
        msg=option.split()
        if(msg[0] == "ls"):
            if(len(option) == 2):
                proxy.root.ngelist1(print_message)
            else:
                msg2 = ' '.join(msg[1:])
                proxy.root.ngelist2(msg2, print_message)

        elif(msg[0] == "count"):
            msg2 = ' '.join(msg[1:])
            proxy.root.itung(msg2, print_message)
        elif(msg[0] == "put"):
            msg2 = ' '.join(msg[1:])
            proxy.root.put(msg2, print_message)
        elif(msg[0] == "get"):
            msg2 = ' '.join(msg[1:])
            proxy.root.get(msg2, print_message)
        elif(msg[0] == "quit"):
            proxy.root.quit(print_message)
            time.sleep(2)
            proxy.close()
        else:
            print("No Command, please retry\n==========================\n")
    
def print_message(string):
    print(string)

if __name__ == '__main__':
    main()