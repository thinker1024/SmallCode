import threading
import socket
import logging
import sys

class Broker():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('10.200.44.44', 22099))
        self.clients_list = []

    def talkToClient(self, ip):
        msg = sys.stdin.readline()
        #self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.sock.sendto(msg, ip)
        logging.info("Sending %s to %s", msg, ip)

    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s: %s', client, msg)
            t = threading.Thread(target=self.talkToClient, args=(client,))
            t.start()

if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.DEBUG)

    b = Broker()
    b.listen_clients()
