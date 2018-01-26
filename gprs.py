#!/usr/bin/env python

import serial
import time

print "\r\n==>To test Quectel M35 GPRS module...\r\n"

# The serial port configuration
ser = serial.Serial(
        port = '/dev/ttyUSB0',
        baudrate = 115200,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = 5,
        xonxoff = None,
        rtscts = None,
        interCharTimeout = None
        )

# Send AT command and check the response string
def SendCMD (cmd_str, check_str):
    ser.reset_input_buffer()
    dataRev = ""
    print "==>Send command %s and verify..." % (cmd_str)
    ser.write(cmd_str)
    ser.write("\r\n")
    time.sleep(1)
    dataRev = ser.read(ser.inWaiting())
    if check_str in dataRev:
        print "==>%s is sent ok" % (cmd_str)
        return 0
    else:
        print "==>%s is sent failed, pls check!" % (cmd_str)
        return 1

# Init nbiot module, ready for the network
def NbiotInit():
    print "Init nbiot module..."
    while SendCMD("ATI", "OK"):
        pass
    while SendCMD("AT+QIFGCNT=0", "OK"):
        pass
    while SendCMD("AT+QICSGP=1,\"CMNET\"", "OK"):
        pass
    while SendCMD("AT+QIMUX=0", "OK"):
        pass
    while SendCMD("AT+QIMODE=0", "OK"):
        pass
    while SendCMD("AT+QIDNSIP=1", "OK"):
        pass
    while SendCMD("AT+QIREGAPP", "OK"):
        pass
    while SendCMD("AT+QIACT", "OK"):
        pass
    return 0

# Establish connection via tcp or udp
def NbiotConnect(protocol, ip, port):
    print "Send data with tcp/udp..."
    cmd_str = "AT+QIOPEN=\"%s\",\"%s\",%d" % (protocol, ip, port)
    while SendCMD(cmd_str, "OK"):
        pass
    while SendCMD("AT+QISEND", ""):
        pass   
     
    return 0

# Send data
def NbiotSend(data):
    ser.reset_input_buffer()
    ser.write(data)

# <CTRL-Z> the key to send data
def NbiotSendCmd():
    ser.reset_input_buffer()
    ser.write(chr(0x1A))
    ser.write("\r\n")

# Close the connection and deact the network
def NbiotClose():
    print "Close the connection..."
    while SendCMD("AT+QICLOSE", "OK"):
        pass
    while SendCMD("AT+QIDEACT", "OK"):
        pass
    return 0

# Main logic
try:
    NbiotInit()
    NbiotConnect("TCP", "logself.vicp.io", 24984)
    
    for i in range(5):
        print "send %d" % (i)
        NbiotSend("12345678")
        NbiotSend("\r\n")
    NbiotSendCmd()

finally:
    NbiotClose()
    ser.close()

