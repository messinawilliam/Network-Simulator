import socket
import sys
import configparser
import random
from time import sleep
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

        host = config[str(num)]['HOST']
        port = int(config[str(num)]['PORT'])
        minDelay = float(config[str(num)]['MINDELAY'])
        maxDelay = float(config[str(num)]['MAXDELAY'])
        return host, port, minDelay, maxDelay


class Client:
    print("Which server do you want to connect to?")
    printSections = Config.sections
    printSections()
    name = input("Enter server name: ")
    configRead = Config.read
    HOST, PORT, minDelay, maxDelay = configRead(name)

    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.settimeout(0.2)

    ttl = struct.pack('b', 1)
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print("Enter 'quit' to exit")
    message = input("Enter message: ")
    while True:
        delay = random.randrange(minDelay, maxDelay)
        sent = soc.sendto(message.encode(), (HOST, PORT))
        sleep(delay/1000)

        while True:
            try:
                data = soc.recvfrom(1024)
                print("Received from server: " + str(data))
                break
            except socket.timeout:
                sys.exit()

        if message == "quit":
            break
        else:
            message = input("Enter message: ")

    soc.close()

if __name__ == '__main__':
    Client()