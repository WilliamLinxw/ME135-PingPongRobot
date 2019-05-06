import serial
import easygui
from time import sleep
import random

ser = serial.Serial('COM3', 57600, timeout=0, parity=serial.PARITY_NONE, rtscts=1)
print(ser)
print(ser.is_open)
sleep(1)


def getData():
    sleep(.05)
    read = ser.read(8)
    # (read[0] == 0) and (read[1]) == 0 and (read[6] == 0) and (read[7] == 0):
    if (read[0] == 0) and (read[1]) == 0 and (read[6] == 0) and (read[7] == 0):
        a = read[2]
        b = read[3]
        c = int.from_bytes([a, b], byteorder='big', signed=True)
        d = int.from_bytes([read[4], read[5]], byteorder='big', signed=True)
        return c, d
    return 0


# 1000, 0, -1000
# we are going to be hitting a ping pong ball, so we need to keep our position for a while
# maybe like .5 seconds?
# when i say stay at 1000, i mean to have you stay at around one thousand.
# +- 15

flag = 1
while True:
    count = getData()
    print(count)
    if flag == 1:

        letter5send = b'-'
        ser.write(letter5send)
        sleep(.05)

        letter9send = b'2'
        ser.write(letter9send)
        sleep(.05)

        letter4send = b'2'
        ser.write(letter4send)
        sleep(.05)

        letter24send = b'0'
        ser.write(letter24send)
        sleep(.05)

        letter6send = b'x'
        ser.write(letter6send)
        sleep(.05)

        letter12send = b'2'
        ser.write(letter12send)
        sleep(.05)

        letter7send = b'0'
        ser.write(letter7send)
        sleep(.05)

        letter10send = b'0'
        ser.write(letter10send)
        sleep(.05)

        letter11send = b'0'
        ser.write(letter11send)
        sleep(.05)

        letter8send = b'y'
        ser.write(letter8send)
        sleep(.05)
        flag = 0

    else:
        continue
