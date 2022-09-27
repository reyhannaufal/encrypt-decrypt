import rpyc
import time

def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    pilihan = " "
    while(pilihan != "quit"):
        pilihan=input("Input command: ")
        msg=pilihan.split()
        if(msg[0] == "ls"):
            if(len(pilihan) == 2):
                proxy.root.ngelist1(cetak)
            else:
                msg2 = ' '.join(msg[1:])
                proxy.root.ngelist2(msg2, cetak)

        elif(msg[0] == "count"):
            msg2 = ' '.join(msg[1:])
            proxy.root.itung(msg2, cetak)
        elif(msg[0] == "put"):
            msg2 = ' '.join(msg[1:])
            proxy.root.put(msg2, cetak)
        elif(msg[0] == "get"):
            msg2 = ' '.join(msg[1:])
            proxy.root.get(msg2, cetak)
        elif(msg[0] == "quit"):
            proxy.root.quit(cetak)
            time.sleep(2)
            proxy.close()
        else:
            print("No Command, please retry\n==========================\n")
    

def noisy(string):
    print('Noisy:', repr(string))

def cetak(string):
    print(string)

if __name__ == '__main__':
    main()