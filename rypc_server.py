import rpyc
import argparse, socket
import sys
import time, os, glob

def main():
    from rpyc.utils.server import OneShotServer
    t = OneShotServer(MyService2, port = 18861)
    t.start()
    t.close()
    sys.exit(0)

class MyService(rpyc.Service):
    def exposed_line_counter(self, fileobj, function):
        print('Client has invoked exposed_line_counter()')
        for linenum, line in enumerate(fileobj.readlines()):
            function(line)
        return linenum + 1

class MyService2(rpyc.Service):
    def exposed_cetak2(self, String, function):
        print('ngirim')
        return function(String)
    def exposed_ngelist1(self, function):
        print("Ngelist...")
        daftar=glob.glob("./*")
        isi=" "
        for i in daftar:
                isi += i + "\n"
        print("Udah ngelistnya yeay")
        return function(isi)
    def exposed_ngelist2(self, String, function):
        print("Ngelist...")
        daftar=glob.glob(String)
        isi=" "
        for i in daftar:
                isi += i + "\n"
        print("Udah ngelistnya yeay")
        return function(isi)
    def exposed_itung(self, String, function):
        print("Ngitung...")
        daftar=glob.glob(String)
        count=0
        for i in daftar:
                count+=1
        print("Udah ngitungnya yeay")
        return function(count)
    def exposed_get(self, String, function):
        print('Ngambil...')
        msg=String.split()
        tempat= ' '.join(msg[:-1])
        tempat2=[tempat, msg[-1]]
        msg2 = '/'.join(tempat2)
        f=open(msg2, "rb")
        b=f.read()
        tulis= "fetch: " + tempat + "\nsize: " + str(len(b)) + "\nlokal: " + msg[-1]
        print("Udah ngambilnya yeay")
        return function(tulis)
    def exposed_put(self, String, function):
        print('Bikin...')
        msg=String.split()
        tempat= ' '.join(msg[1:])
        tempat2=[tempat, msg[0]]
        msg2 = '/'.join(tempat2)
        f=open(msg2, "x")
        f.close()
        tulis= "put: " + tempat + "\nlokal: " + msg[0]
        print("Udah bikinnya yeay")
        return function(tulis)
    def exposed_quit(self, function):
        print('Shutting down...')
        function("Bye bye")
        sys.exit(0)

if __name__ == '__main__':
    main()