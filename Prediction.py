from collections import deque
import numpy as np
import cv2
import time
from timeit import default_timer as timer
import warnings
import matplotlib.pyplot as plt
import math

warnings.simplefilter('ignore', np.RankWarning)
# warnings.filterwarnings('error')
# np.seterr(all='raise')


#   Set the threshold for color red in HSV
redLower = np.array([35, 43, 46])  # currently purple
redUpper = np.array([77, 255, 255])


#   Set the default x direction distance
# X = 200
#   Initialize the length for tracking coordinates
my_buffer = 64
ptsXY = deque(maxlen=my_buffer)  # comes from laptop camera
ptsYZ = deque(maxlen=my_buffer)  # comes from Josh camera


x_camera_0 = deque(maxlen=my_buffer)
y_camera_0 = deque(maxlen=my_buffer)
Y_camera_1 = deque(maxlen=my_buffer)
Z_camera_1 = deque(maxlen=my_buffer)

#   Turn on the camera
camera1 = cv2.VideoCapture(0)  # laptop Camera <-- will be looking at the ball
camera2 = cv2.VideoCapture(1)  # Josh's Camera <-- will be in front of the camera

#   Wait for 2 seconds
time.sleep(2)

# ------
time_lst = np.array([0])
timeTilPred = 0
movement = np.array([0])
other_camera = np.array([0])
# ------

#   Detect color red
while True:
    # ----
    before = timer()
    # ----
    #   Read the frames
    _, frame = camera1.read()
    _, frame2 = camera2.read()
    #   Change the frames to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    #   Build a mask based on threshold
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask2 = cv2.inRange(hsv2, redLower, redUpper)
    #   Erosion
    mask = cv2.erode(mask, None, iterations=2)
    mask2 = cv2.erode(mask2, None, iterations=2)
    #   Dilation, remove the noise by erosion and dilation
    mask = cv2.dilate(mask, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)
    #   Detect the contour
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #   Initialize the centroid
    center = None
    center2 = None
    #   If there is a contour
    if len(cnts) > 0 :
        #   Find the contour with the largest area
        c = max(cnts, key = cv2.contourArea)
        #   Determine the circumcircle of the largest contour
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #   Calculate the moment of the contour
        M = cv2.moments(c)
        #   Calculate the centroid
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        #   Plot only when the radius is greater than 0
        if radius > 0:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #   print('x coordinate: %s, y coordinate: %s'%(x, y))
            #   Add the centroid to the left of the list
            ptsXY.appendleft(center)
            x_camera_0.appendleft([ptsXY[0][0]])
            y_camera_0.appendleft([ptsXY[0][1]])
    if len(cnts2) > 0:
        #   Find the contour with the largest area
        c2 = max(cnts2, key=cv2.contourArea)
        #   Determine the circumcircle of the largest contour
        ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
        #   Calculate the moment of the contour
        M2 = cv2.moments(c2)
        #   Calculate the centroid
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        #   Plot only when the radius is greater than 0
        if radius2 > 0:
            cv2.circle(frame2, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)
            cv2.circle(frame2, center2, 5, (0, 0, 255), -1)
            #   print('x coordinate: %s, y coordinate: %s'%(x, y))
            #   Add the centroid to the left of the list
            ptsYZ.appendleft(center2)
            Y_camera_1.appendleft([ptsYZ[0][0]])
            Z_camera_1.appendleft([ptsYZ[0][1]])
    # res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('XY', frame)
    cv2.imshow('YZ', frame2)
    #   Exit when press the esc button

    after = timer()
    tme = after - before
    time_lst = np.append(time_lst, [tme])
    timeTilPred += tme
    # print(ptsXY, len(ptsXY))
    if timeTilPred > .25:
        if len(ptsXY) > 6:
            timeTilPred = 0
            ## TODO: Complete all prediction algorithms here
            ## We want to predict .25 seconds ahead
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    # print(len(ptsXY) * 2 // 4)
                    # print(len(ptsXY) * 3 // 4)
                    # x = np.array([ptsXY[0][0], ptsXY[(len(ptsXY) // 4)][0], ptsXY[(len(ptsXY) * 2 // 4)][0], ptsXY[(len(ptsXY) * 3 // 4)][0], ptsXY[len(ptsXY) - 1][0]])
                    # y = np.array([ptsXY[0][1], ptsXY[len(ptsXY) // 4][1], ptsXY[len(ptsXY) * 2 // 4][1], ptsXY[len(ptsXY) * 3 // 4][1], ptsXY[len(ptsXY) - 1][1]])
                    x = np.array(x_camera_0)
                    y = np.array(y_camera_0)
                    x1 = np.concatenate(x)
                    y1 = np.concatenate(y)
                    z1 = np.polyfit(x1, y1, 2)
                    #z = np.polyder(z)
                    polyPredict1 = np.poly1d(z1)
                    # polyPredict = np.polyder(polyPredict)
                    # print(z)
                    moveY = polyPredict1(640)
                    if moveY > 480 or moveY < 0:
                        continue
                    movement = np.append(movement, [moveY])
                    print('Last Y is',moveY)
                except Warning:
                    moveY = 0
        if len(ptsYZ) > 6:
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    Y = np.array(Y_camera_1)
                    Z = np.array(Z_camera_1)
                    Y1 = np.concatenate(Y)
                    Z1 = np.concatenate(Z)
                    z2 = np.polyfit(Y1, Z1, 2)
                    polyPredict2 = np.poly1d(z2)
                    delta = z2[1] * z2[1] - 4 * z2[0] * (z2[2] - 480)
                    if delta > 0:
                        if Z[0] > Z[1]:
                            Depth1 = (-z2[1] + math.sqrt(delta)) / (2 * z2[0])
                            print('Depth 1 is', Depth1)
                        else:
                            Depth2 = (-z2[1] - math.sqrt(delta)) / (2 * z2[0])
                            print('Depth 2 is', Depth2)
                    else:
                        print('No root')
                    other_camera = np.append(other_camera, [max(Z[0], Z[1])])
                except Warning:
                    Depth1 = 0
                    Depth2 = 0
        # y2 = np.array([ptsYZ[0][0], ptsYZ[1][0], ptsYZ[2][0], ptsYZ[3][0]])
        # z2 = np.array([ptsYZ[0][1], ptsYZ[1][1], ptsYZ[2][1], ptsYZ[3][1]])
        # x2 = np.polyfit(x2, y2, 2)
        # polyPredict = np.poly1d(x2)
        # polyPredict = np.polyder(polyPredict)
        # moveZ = polyPredict(.25)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

#   Release the camera
camera1.release()
#   Destroy the windows
cv2.destroyAllWindows()
print(1/np.mean(time_lst))

plt.plot(movement, 'r-', label = 'ptsXY')
plt.plot(other_camera, 'k--', label = 'ptsYZ')
plt.show()