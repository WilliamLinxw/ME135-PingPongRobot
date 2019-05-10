import matplotlib
import matplotlib as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time
from collections import deque
import cv2
import time
from timeit import default_timer as timer
import warnings
import math
import serial
from math import tan
from math import pi
import sys

#   Initialize the serial port
#   --------
ser = serial.Serial('COM3', 57600, timeout=0, parity=serial.PARITY_NONE, rtscts=1) # uncomment once PSOC exists
print(ser.is_open)
time.sleep(1)
#   --------



warnings.simplefilter('ignore', np.RankWarning)
# warnings.filterwarnings('error')
# np.seterr(all='raise')


#   Set the threshold for color black in HSV space`
blackLower = np.array([90, 155, 20])
blackUpper = np.array([110, 255, 200])


#   Initialize the length for tracking coordinates
my_buffer = 64
ptsYZL = deque(maxlen=my_buffer)  # comes from laptop camera (bad coords)
ptsXZJ = deque(maxlen=my_buffer)  # comes from Josh camera (bad coords)
ptsRealX = deque(maxlen=my_buffer)
ptsRealY = deque(maxlen=my_buffer)
ptsRealZ = deque(maxlen=my_buffer)

#   Turn on the camera
camera1 = cv2.VideoCapture(1)  # Josh's Camera <-- will be looking at the ball, the ball will be crossing the frame
camera2 = cv2.VideoCapture(0)  # Laptop's Camera <-- will be in front of the camera, the ball will be in the frame

#   Wait for 2 seconds
time.sleep(2)

#   Make the camera data Arrays

# ---------------------------
time_lst = np.array([0])
timeTilPrediction = 0
bufferTime = 0
movement = np.array([0])
other_camera = np.array([0])
# ---------------------------

# For testing purposes, the Matplotlib graph
# ---------------------------
showXCoords = np.array([])
showYCoords = np.array([])
showZCoords = np.array([])
predictedXArray = np.array([])
predictedZArray = np.array([])
encoderDataUpDown = np.array([])
encoderDataLeftRight = np.array([])
# ---------------------------

# the function to get the data from the psoc. IE the reading function
# ---------------------------
def getData():
    # time.sleep(.03) # No longer will use this line
    # time.sleep(.05)
    read = ser.read(8)
    if (read[0] == 0) and (read[1]) == 0 and (read[6] == 0) and (read[7] == 0):
        a = read[2]
        b = read[3]
        c = int.from_bytes([a, b], byteorder='big', signed=True)
        d = int.from_bytes([read[4], read[5]], byteorder='big', signed=True)
        ser.reset_input_buffer()
        return c, d
    ser.reset_input_buffer()
    print("didnt get iterable")
    return (0, 0)
# ---------------------------

# Make the function to give the data to the PSOC
# TODO: get the working function from the other file
# ---------------------------
def sendData(upAndDown, LeftAndRight):
    # changed the sending to only sleep for .01, instead of .05
    if upAndDown > 100:
        upAndDown = 99

    firstByte = bytes(str(upAndDown // 10), 'ascii')
    secondByte = bytes(str(upAndDown % 10), 'ascii')
    # letter4send = b'1'
    ser.write(firstByte)
    # time.sleep(.003)
    ser.write(secondByte)
    # time.sleep(.003)
    letter6send = b'x'
    ser.write(letter6send)
    # time.sleep(.003)
    # ser.reset_output_buffer() # this might be needed

    # print(highNumber // 1000)
    if LeftAndRight < 0:
        LeftAndRight = 0
    if LeftAndRight > 9999:
        LeftAndRight = 9999

    largestDigit = bytes(str(LeftAndRight // 1000), 'ascii')
    ser.write(largestDigit)
    # time.sleep(.003)
    LeftAndRight = LeftAndRight % 1000
    # print(LeftAndRight // 100)
    hundreds = bytes(str(LeftAndRight // 100), 'ascii')
    ser.write(hundreds)
    # time.sleep(.003)
    LeftAndRight = LeftAndRight % 100
    # print(LeftAndRight // 10)
    tens = bytes(str(LeftAndRight // 10), 'ascii')
    ser.write(tens)
    # time.sleep(.003)
    LeftAndRight = LeftAndRight % 10
    # print(LeftAndRight // 1)
    ones = bytes(str(LeftAndRight // 1), 'ascii')
    ser.write(ones)
    # time.sleep(.003)

    letter8send = b'y'
    ser.write(letter8send)
    time.sleep(.001)
    ser.reset_output_buffer()
    return
# ---------------------------

# Basic control for the flipping motor
# ---------------------------
def flippingMotor():
    # number = [7]
    # bts = bytes(number)
    ser.reset_output_buffer()
    bts = b'H'  # will now send an H whenever it runs, to match the code Caeser did
    ser.write(bts)
    # time.sleep(0.001)
    ser.reset_output_buffer()
    # print("sent a flip")
    # time.sleep(.005) # eliminate this line for now because there should be no sending conflict
    return
# ---------------------------


# need to make a function that takes the data from the deque and returns an array
# ---------------------------
def toLst(dequeArray):
    returnLst = []
    # for integer, _ in enumerate(dequeArray):
    for _, item in enumerate(dequeArray):
        returnLst.append(item)
        # print(type(item))
    return returnLst


# ---------------------------
# Define camera constants (NOTE: make sure that the robot is a distance 2A from the laptop camera)
# NOTE: these are in decimeters. Why? because that is what I chose
# ---------------------------
A = 17.78  #
B = 14.732  # 58in
C = 10.16  #
distanceToRobot = 30.734
LRMoveTick = .02  # .013, .015, .022
startingPositionHorizontal = B - 3.91
debuggingCount = 0
flag = True
# ---------------------------

#   Detect color black

# set the robot at a certain value
initSend = int((startingPositionHorizontal / LRMoveTick) // 1)
sendData(0, initSend)  # send the data to start the robot in the middle6
LeftAndRight = 0



LARGE_FONT = ("Times New Roman", 50)
NORM_FONT = ("Times New Roman", 40)
SMALL_FONT = ("Times New Roman", 30)
style.use("ggplot")

class WelcomePage(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Ping Pong Bot GUI """, font=LARGE_FONT)
        label.pack(pady=100, padx=100)

        button1 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Do you agree to gurantee us an A?", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree",
                             command=lambda: controller.show_frame(PageTwo))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="You Agreed to Give Us An A!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Start Video", command=lambda: welcome.destroy())
        button1.pack()


welcome = WelcomePage()
welcome.mainloop()
# now for the real shit: the while loop
# ------------------------------------------------------------------

sendData(0, initSend)
while True:

    if bufferTime > .1:
        upAndDown, LeftAndRight = getData()
        encoderDataLeftRight = np.append(encoderDataLeftRight, [LeftAndRight])
        if upAndDown > 30:
            upAndDown = 30
        encoderDataUpDown = np.append(encoderDataUpDown, [upAndDown])
        # print(upAndDown, " <-  upAndDown === ", debuggingCount, "==== left and right ->", LeftAndRight)
        bufferTime = 0
        # debuggingCount += 1

    #   --------
    before = timer()
    #   --------
    #   Read the frames
    _, frame = camera1.read()
    _, frame2 = camera2.read()

    #   Change the frames to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    #   Build a mask based on threshold
    mask = cv2.inRange(hsv, blackLower, blackUpper)
    mask2 = cv2.inRange(hsv2, blackLower, blackUpper)

    #   Erosion
    mask = cv2.erode(mask, None, iterations=2)
    mask2 = cv2.erode(mask2, None, iterations=2)

    #   Dilation, remove the noise by erosion and dilation
    mask = cv2.dilate(mask, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)

    #   Detect the contour
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #   Initialize the centroid
    center = None
    center2 = None

    #   If there is a contour
    if len(contours) > 0:  # Josh's camera for ball crossing the frame
        #   Find the contour with the largest area
        c = max(contours, key=cv2.contourArea)

        #   Determine the circle of the largest contour
        ((y, z1), radius) = cv2.minEnclosingCircle(c)

        #   Calculate the moment of the contour
        M = cv2.moments(c)

        #   Calculate the centroid
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

        #   Plot only when the radius is greater than 0
        if radius > 0:
            cv2.circle(frame, (int(y), int(z1)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            # print('y coordinate: %s, z1 coordinate: %s'%(y, z1))

            #  Add the centroid to the left of the list
            ptsYZL.appendleft(center)

    if len(contours2) > 0:
        #   Find the contour with the largest area
        c2 = max(contours2, key=cv2.contourArea)

        #   Determine the circle of the largest contour
        ((x, z2), radius2) = cv2.minEnclosingCircle(c2)

        #   Calculate the moment of the contour
        M2 = cv2.moments(c2)

        #   Calculate the centroid
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))

        #   Plot only when the radius is greater than 0
        if radius2 > 0:
            cv2.circle(frame2, (int(x), int(z2)), int(radius2), (0, 255, 255), 2)
            cv2.circle(frame2, center2, 5, (0, 0, 255), -1)
            #   print('y coordinate: %s, z1 coordinate: %s'%(y, z2))

            #   Add the centroid to the left of the list
            ptsXZJ.appendleft(center2)

    #   Covert pixel coordinates (x,y,z1,z2) to real world coordinates (X,Y,Z)
    # since we are adding to the front of the list, we are always taking the most recent coords
    # this works:
    if len(ptsXZJ) > 1 and len(ptsYZL) > 1:
        x_convert = ptsXZJ[0][0]  # take most recent recorded X coord from Josh Camera
        y_convert = ptsYZL[0][0]  # the most recent recorded Y coord from Laptop camera
        z1_convert = ptsYZL[0][1]  # the most recorded Z coord from the laptop camera
        # print("The pixel coordinate of x is: ", x_convert)
        # print("The pixel coordinate of y is: ", y_convert)
        # print("The pixel coordinate of z1 is: ", z1_convert)
        X_real = (B + tan(1.92e-3*x_convert - .614)*A) / (1 - tan(1.92e-3*x_convert - .614)*tan(1.415 - 2.2111e-3*y_convert - .708))
        Y_real = tan(1.415 - 2.21e-3*y_convert - .708)*X_real + A
        Z_real = tan(0.941 - 1.96e-3*z1_convert - .4704)*X_real + C
        Real_world_coordinate = (X_real, Y_real, Z_real)
        # print("The real X coordinate is: ", X_real)
        # print("The real Y coordinate is: ", Y_real)
        # print("The real Z coordinate is: ", Z_real)
        # ptsXYZ.appendleft(Real_world_coordinate)

        ptsRealX.appendleft(Real_world_coordinate[0])
        # print("This is real x coords points", ptsRealX)
        ptsRealY.appendleft(Real_world_coordinate[1])
        ptsRealZ.appendleft(Real_world_coordinate[2])

        showXCoords = np.append(showXCoords, [Real_world_coordinate[0]])
        showYCoords = np.append(showYCoords, [Real_world_coordinate[1]])
        showZCoords = np.append(showZCoords, [Real_world_coordinate[2]])

        if Real_world_coordinate[1] > (A + 2) and flag:
            flippingMotor()
            flag = False

    cv2.imshow('YZ', frame)
    cv2.imshow('XZ', frame2)
    after = timer()
    tme = after - before
    time_lst = np.append(time_lst, [tme])
    timeTilPrediction += tme
    bufferTime += tme
    #   print(ptsXY, len(ptsXY))
    # moveX_array = np.array([0])
    # moveY_array = np.array([0])
    # moveX = 0
    # moveY = 0
    #
    # Prediction Starts

    if len(ptsXZJ) > 2 and len(ptsYZL) > 2:
        # print(debuggingCount)
        if timeTilPrediction > .0025:
            timeTilPrediction = 0  # Once this part of code is executed, we will start the time again from zero
            # the following code will take our 64 coords points and put them into a python list
            # we will then use this list to make a numpy A array for our linear least squares
            realXCoords = toLst(ptsRealX)
            # print("This is real X coords =======", realXCoords)
            realYCoords = toLst(ptsRealY)
            realZCoords = toLst(ptsRealZ)

            # x = np.array(realXCoords, dtype=np.float64)
            # xArray = np.array(realXCoords, dtype='float64')
            xArray = np.array(realXCoords)
            del realXCoords
            yArray = np.array(realYCoords)
            del realYCoords
            # print("This is the X Array", xArray, "End X array ==========")
            AMatrix = np.vstack((xArray, np.ones(len(xArray)))).T  # this is our linear least squares matrix
            # print("this is the A matrix", AMatrix, "End A matrix ~~~~~~~~~~~~~~~~")
            del xArray
            # A.metrics = []
            # A.astype(np.float32)
            # A = np.matrix(x, np.ones(len(x), dtype=np.float64), dtype=np.float64).T
            m, b = np.linalg.lstsq(AMatrix, yArray, rcond=None)[0]  # a tuple to satisfy the equation y = mx + b
            del AMatrix

            # assuming our (zero, zero) is on the same line as our laptop cameray
            """
                                        [Robot]
                ⌄     |~~~~~~~~~~~~~~~~~~~{X}~~~~~~~~~~~~~~~~~~~~~
                      |                  /
                      |                 /
                A     |                /
                      |               /
                ^     |              /
            [Josh's]  |             /
            camera]   |            /
                ⌄     |           /
                      |          /
                A     |         /
                      |        /
                      |_______/__________________________________
                ^      [-    B     -][laptop camera][-    B     -]
                _
              / ⌄ \
             |>{C}<|
              \ ^ /
            The above is what the following line of code predicts:
            """
            # distanceToRobot = 25.9
            predictedX = (distanceToRobot - b) / m  # change to 2A when doing the demo
            if predictedX < 0:
                predictedX = 0
            if predictedX > 17:
                predictedX = 17
            predictedXArray = np.append(predictedXArray, [predictedX])
            # print("This is the number where it will land", predictedX)

            # from above we already have y
            # we now need z
            zArray = np.array(realZCoords, dtype='float32')
            function = np.polyfit(yArray, zArray, 2)
            polynomial = np.poly1d(function)
            predictedZ = polynomial(20.5)  # change to 2A for the
            # the Threshold for the max arm length
            if predictedZ < 4.826:
                predictedZ = 4.826
            if predictedZ > 7.5:
                predictedZ = 7.5

            predictedZArray = np.append(predictedZArray, [predictedZ])
            del yArray
            del zArray
            # sendData(up and down, left and right)
            sendXMotorCount = int((predictedX / LRMoveTick) // 1)
            if sendXMotorCount < 10:
                sendXMotorCount = initSend

            sendData(int(((predictedZ - 4.826) / .18) // 1), sendXMotorCount)

            # print("we are sending: ", sendXMotorCount, ". We currently have: ", LeftAndRight)
            # print("after if debugging count", debuggingCount)

    # print("These are the coordinates. X position is: ", moveX, "\n", "Y Position is: ", moveY)
    # sentData = ser.write([moveX, moveY])
    # print(sentData)
    # # send one array of data at a time, will block until the number of bytes is read
    # # Ethan thinks the while loop will not continue until after the number of bytes is read
    # # but Ethan could be wrong
    # # Ethan is wrong.
    # byteArray = ser.read(16)
    # print(byteArray)

    # Exit when press the esc button
    k = cv2.waitKey(3) & 0xFF
    if k == 27:
        break

    if k == 32:
        sys.exit()
    #

#   Release the camera
camera1.release()
camera2.release()
#   Destroy the windows
cv2.destroyAllWindows()
# print(1/np.mean(time_lst))
sendData(1, 10)
time.sleep(3)  # time.sleep is in seconds
# print("below this line is writing")
killbyte = b'K'
ser.reset_output_buffer()
ser.write(killbyte)
print("sent killbyte")
xy = open("xy.txt", "w+")

# file name here = open() <- take in a string to the path of the file, the other argument w mean write, plus mean create

length = min(showXCoords.size, showYCoords.size)

for _, integer in enumerate(range(length)):
    writeString = "{}, {}".format(showXCoords.astype(int)[integer], showYCoords.astype(int)[integer]) # {} is a format tool
    xy.write(writeString)
    xy.write("\r\n")

xy.close()

xz = open("xz.txt", "w+")

# file name here = open() <- take in a string to the path of the file, the other argument w mean write, plus mean create

length = min(showXCoords.size, showZCoords.size)

for _, integer in enumerate(range(length)):
    writeString = "{}, {}".format(showXCoords.astype(int)[integer], showZCoords.astype(int)[integer]) # {} is a format tool
    xz.write(writeString)
    xz.write("\r\n")

xz.close()

yz = open("yz.txt", "w+")

# file name here = open() <- take in a string to the path of the file, the other argument w mean write, plus mean create

length = min(showXCoords.size, showZCoords.size)

for _, integer in enumerate(range(length)):
    writeString = "{}, {}".format(showYCoords.astype(int)[integer], showZCoords.astype(int)[integer]) # {} is a format tool
    yz.write(writeString)
    yz.write("\r\n")

yz.close()

predicted_xz = open("predicted_xz.txt", "w+")

# file name here = open() <- take in a string to the path of the file, the other argument w mean write, plus mean create

length = min(predictedXArray.size, predictedZArray.size)

for _, integer in enumerate(range(length)):
    writeString = "{}, {}".format(predictedXArray.astype(int)[integer], predictedZArray.astype(int)[integer]) # {} is a format tool
    predicted_xz.write(writeString)
    predicted_xz.write("\r\n")

predicted_xz.close()

enc_Data = open("enc_Data.txt", "w+")

# file name here = open() <- take in a string to the path of the file, the other argument w mean write, plus mean create

length = min(encoderDataLeftRight.size, encoderDataUpDown.size)

for _, integer in enumerate(range(length)):
    writeString = "{}, {}".format(encoderDataLeftRight.astype(int)[integer], encoderDataUpDown.astype(int)[integer]) # {} is a format tool
    enc_Data.write(writeString)
    enc_Data.write("\r\n")

enc_Data.close()


# plt.plot(showXCoords, showYCoords, 'o-', label='XY axis')
# plt.xlabel('real life x coords')
# plt.ylabel('real life y coords')
# plt.show()
# plt.plot(showYCoords, showZCoords, 'ko-', label='YZ axis')
# plt.xlabel('real life y coords')
# plt.ylabel('real life z coords')
# plt.show()
#
# plt.plot(predictedXArray, 'go-', label='predicted x ')
# plt.xlabel('time')
# plt.ylabel('predicted x location')
# plt.show()
# plt.plot(predictedZArray, 'bo-', label='predicted z')
# plt.xlabel('time')
# plt.ylabel('predicted z location')
# plt.show()

# sendData(0, initSend)

# sendData(1, 10)

# plt.plot(moveX_array, moveY_array, 'r--', label='raw coordinates')
# plt.show()



# ------------------------------------------------------------------
# print("made it out of the loop")
f = Figure()
a = f.add_subplot(211)
b = f.add_subplot(212)

g = Figure()
c = g.add_subplot(221)
d = g.add_subplot(223)
e = g.add_subplot(222)
h = g.add_subplot(224)


def popupmsg(msg):
    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=SMALL_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def animatea(i):
    pullData = open("enc_Data.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    zList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, z = eachLine.split(',')
            xList.append(int(x))
            zList.append(int(z))
    a.clear()

    length = len(xList)
    intv = 16 * 10 ** (-3)
    t = numpy.linspace(0, length - 1, length) * intv
    a.plot(t, xList, marker="o")

    title = "Horizontal movement of the BOT"
    ylabel = "X Position (mm)"
    a.set_title(title)
    a.set_ylabel(ylabel)


def animateb(i):
    pullData = open("enc_Data.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    zList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, z = eachLine.split(',')
            xList.append(int(x))
            zList.append(int(z))
    b.clear()

    length = len(xList)
    intv = 16 * 10 ** (-3)
    t = numpy.linspace(0, length - 1, length) * intv
    b.plot(t, zList, marker="o")

    title = "Vertical movement of the BOT"
    xlabel = "Time (s)"
    ylabel = "Z Position (mm)"
    b.set_title(title)
    b.set_xlabel(xlabel)
    b.set_ylabel(ylabel)


def animatec(i):
    pullData = open("xy.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    c.clear()

    c.plot(xList, yList, marker="o")

    title = "x-y Chart of the Ping Pong"
    xlabel = "X Position (mm)"
    ylabel = "Y Position (mm)"
    c.set_title(title)
    c.set_ylabel(ylabel)


def animated(i):
    pullData = open("xz.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    d.clear()

    d.plot(xList, yList, marker="o")

    title = "x-z Chart of the Ping Pong"
    xlabel = "X Position (mm)"
    ylabel = "Z Position (mm)"
    d.set_title(title)
    d.set_ylabel(ylabel)


def animatee(i):
    pullData = open("yz.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    e.clear()

    e.plot(xList, yList, marker="o")

    title = "y-z Chart of the Ping Pong"
    xlabel = "Y Position (mm)"
    ylabel = "Z Position (mm)"
    e.set_title(title)
    e.set_ylabel(ylabel)


def animateh(i):
    pullData = open("predicted_xz.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    h.clear()

    h.plot(xList, yList, marker="o")

    title = "x-z Chart of the Prediction"
    xlabel = "X Position (mm)"
    ylabel = "Z Position (mm)"
    h.set_title(title)
    h.set_ylabel(ylabel)





class PiongPongBotGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "PongPongBot GUI")
        # tk.Tk.iconbitmap (self, default="")
        #         self.vid = MyVideoCapture(self.video_source)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Setting", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def client_exit(self):
        exit()


def qf(param):
    print(param)




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=100, padx=100)

        button1 = ttk.Button(self, text="Ball Trajectory Tracking",
                             command=lambda: controller.show_frame(PageTwo))
        button1.pack()

        button2 = ttk.Button(self, text="BOT Movement Tracking",
                             command=lambda: controller.show_frame(PageThree))
        button2.pack()

    #         videoCapture = ttk.Button(self, text="video capture",


#                             command=lambda:controller.show_frame(MyVideoCapture))
#         videoCapture.pack()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Trajectory Tracking Charts", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home Page",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()

        canvas = FigureCanvasTkAgg(g, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BOT Movement Tracking Charts", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home Page",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = PiongPongBotGUI()
app.geometry("1920x1080")
ani = animation.FuncAnimation(f, animatea, interval=1000)
anib = animation.FuncAnimation(f, animateb, interval=1000)
anic = animation.FuncAnimation(g, animatec, interval=1000)
anie = animation.FuncAnimation(g, animatee, interval=1000)
anid = animation.FuncAnimation(g, animated, interval=1000)
anih = animation.FuncAnimation(g, animateh, interval=1000)
app.mainloop()
