import serial
import time
import sys
import random


cmd_on = "0000ffffe411020001"
cmd_off = "0000ffffe411020000"
cmd_color = "0000ffffe4110201010000ff0000"
cmd_hue = "0000ffffe41102010100ff000000"
cmd_adv_on = "00000000e41102fc01"
cmd_adv_off = "00000000e41102fc01"
sn = "000000"
header = "00021410000400121500"

def sn_gen(countx) :
    snx = hex(countx)
    snx = snx[2:]
    if len(snx)%2 != 0 :
        snx = '0'+snx
    while len(snx) != 6 :
        snx = '0'+snx
    snx = snx[4:6] + snx[2:4] + snx[0:2]
    return snx

def main():

    ser = serial.Serial(
            #port = "/dev/ttymxc5",
            port = "/dev/ttyUSB0",
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
        count = random.randint(0,255)
        sn = sn_gen(count)
 
        if sys.argv[1] == "autotest" :
           
            while True:
                if count > 0xFFFFFC :
                    count = 0
                
                time.sleep(3)
                ser.write((header+sn+cmd_on).decode("hex"))
                count = count + 1
                sn = sn_gen(count)
                print sn
                time.sleep(3)

                ser.write((header+sn+cmd_off).decode("hex"))
                count = count + 1
                sn = sn_gen(count)
                print sn
                time.sleep(3)

                ser.write((header+sn+cmd_color).decode("hex"))
                count = count + 1
                sn = sn_gen(count)
                print sn
                time.sleep(3)

                ser.write((header+sn+cmd_hue).decode("hex"))
                count = count + 1
                sn = sn_gen(count)
                print sn
        if sys.argv[1] == "on" :
            ser.write((header+sn+cmd_on).decode("hex"))
        if sys.argv[1] == "off":
            ser.write((header+sn+cmd_off).decode("hex"))
        if sys.argv[1] == "color":
            ser.write((header+sn+cmd_color).decode("hex"))
        if sys.argv[1] == "hue":
            ser.write((header+sn+cmd_hue).decode("hex"))
        if sys.argv[1] == "update":
            ser.write((header+sn+cmd_adv_on).decode("hex"))
            
    finally:
        ser.close()


main()
