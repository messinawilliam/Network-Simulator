import socket
import sys
from _thread import *
import threading
import configparser
import struct

class Config:
    def sections():
        config = configparser.ConfigParser()
        config.read('databaseConfig.txt')

        sections = config.sections()
        print(f'Sections: {sections}')

        for section in sections:

            if config.has_section(section):
                print(f'Config file has section {section}')
            else:
                print(f'Config file does not have section {section}')

    def read(num):
        config = configparser.ConfigParser()
        config.read('databaseConfig.txt')

        HOST = config[str(num)]['HOST']
        PORT = int(config[str(num)]['PORT'])
        return HOST, PORT



class Server:
    print("Which server do you want to connect to?")
    printSections = Config.sections
    printSections()
    name = input("Enter server name: ")
    configRead = Config.read
    HOST, PORT = configRead(name)

    lock = threading.Lock()

    def threaded(client):
        while True:
            data = client.recv(1024)
            if not data:
                print('Not received')
                lock.release()
                break
            data = data[::-1]
            client.sendto(data.encode())
        client.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Socket created")

    try:
        s.bind((HOST, PORT))
        print("Socket bound")
    except:
        print("Bind failed")
        sys.exit()

    group = socket.inet_aton(HOST)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        conn, addr = s.recvfrom(1024)
        lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (conn,))
        s.sendto('ack', addr).encode()
    s.close()


if __name__ == '__main__':
    Server()