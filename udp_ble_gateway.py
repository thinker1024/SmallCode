################################
## Version: V1.0              ##
## Author: Tao Yang           ##
## Date: 2018.01              ##
################################

import threading
import socket
import logging
import sys
import time
import serial

sn = "332211"
src = "0000"
dst = "ffff"
opcode = "e41102"
code_onoff = "00"
code_color = "01"
light_on = "01"
light_off = "00"
color_on = "01"
color_off = "00"
color_white = "00"
color_hue = "00"
color_rgb = "ff0000"

code_adv = "fc"

#header = "00021410000400121500"
header = ""

cmd_on = src+dst+opcode+code_onoff+light_on
cmd_off = src+dst+opcode+code_onoff+light_off
cmd_color = src+dst+opcode+code_color+color_on+color_white+color_hue+color_rgb
cmd_hue = src+dst+opcode+code_color+color_on+color_white+"60"+"000000"
cmd_adv = src+"0000"+opcode+code_adv+"01"

#cmd_on = "3322110000ffffe411020001"
#cmd_off = "3322110000ffffe411020000"
#cmd_color = "3322110000ffffe4110201010000ff0000"
#cmd_hue = "3322110000ffffe4110201010030000000"

def int2HexStr(count) :
    sn = hex(count)
    sn = sn[2:]
    if len(sn)%2 != 0 :
        sn = '0'+sn
    return sn

def HexShow(argv):
    result = ''
    xLen = len(argv)
    for i in xrange(xLen):
        temp = ord(argv[i])
        hhex = '%02x'%temp
        result += hhex+''
    return result


class Broker():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('10.100.3.112', 22099))
        self.clients_list = []

    def talkToClient(self, ip):
        #msg = sys.stdin.readline()
        msg = ser.read(ser.inWaiting())
        msg = HexShow(msg)
        #self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.sock.sendto(msg, ip)
        logging.info("Sending %s to %s", msg, ip)

    def listen_clients(self, ser):
        count = 0
        while True:
            msg, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s: %s', client, msg)
            
            if count == 0xFFFFFF :
                count = 0
            sn = int2HexStr(count)
            while len(sn) != 6 :
                sn = '0' + sn
            sn = sn[4:6] + sn[2:4] + sn[0:2]
            logging.info("sn: %s", sn)
            
            if msg == 'on': 
                ser.write((header+sn+cmd_on).decode("hex"))
                count = count + 1
            if msg == 'off':
                ser.write((header+sn+cmd_off).decode("hex"))
                count = count + 1
            if msg == 'color':
                ser.write((header+sn+cmd_color).decode("hex"))
                count = count + 1
            if msg == 'hue':
                ser.write((header+sn+cmd_hue).decode("hex"))
                count = count + 1
            if msg == 'adv':
                ser.write((header+sn+cmd_adv).decode("hex"))
                count = count + 1


            #time.sleep(0.1)
            #dataRecv = ser.read(ser.inWaiting())
            #print dataRecv

            t = threading.Thread(target=self.talkToClient, args=(client,))
            t.start()

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)
    ser = serial.Serial( 
            port = "/dev/ttymxc5",
#            port = "/dev/ttyUSB0",
            baudrate = 115200,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = 0.5,
            xonxoff = None,
            rtscts = None,
            interCharTimeout = None
            )

    try:
	ser.isOpen()
        b = Broker()
        b.listen_clients(ser)
    finally:
        ser.close()

