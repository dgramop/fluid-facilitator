import cv2
import serial
import struct

port = 'COM6'
baudrate = 9600

srl = serial.Serial(port, baudrate, timeout=5)
srl.read(2)
srl.reset_input_buffer()

w = 640
l = 480
deadzone = 30

countdown = 0

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()

aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

capture = cv2.VideoCapture(1)

def move_one(direction):
    data = struct.pack('>cIc', bytes(direction, 'ASCII'), 1, b"\n")
    srl.write(data)
    res = srl.read().decode("ASCII")
    # if res == 'L':
    #     print('Limit Reached')
    # else:
    #     print('Fine')

def spray(seconds):
    data = struct.pack('>cIc', b('P'), seconds * 1000, b"\n")
    srl.write(data)
    srl.read().decode('ASCII')


while True:
    # read() returns false for ret if a frame cant be captured for some reason
    ret, frame = capture.read()

    if not ret:
        break

    # Detect them squares
    corners, ids, rejected_points = aruco_detector.detectMarkers(frame)

    center = 0

    #cv2.flip(frame, 1, frame)

    # Draw them if there is at least one
    if len(corners) > 1:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        x1 = corners[0][0][0][0]
        x2 = corners[0][0][2][0]
        center = (x1 + x2) / 2
        center_coords = (width-(width-center), height-(height-center))
        #print(corners[0].mean())

    if corners and center!=0:
        if (width/2 - deadzone) < center < (width/2 + deadzone):
            countdown += 1
            # print("DEADZONE")
        elif int(center) < w/2:
            move_one('L')
            countdown = 0
            print('l')
        else:
            move_one('R')
            countdown = 0
            print('r')

    if countdown == 150:
        print('spray')
        spray(2)

    # Show the result
    cv2.imshow('frame', frame)

    x, y, width, height = cv2.getWindowImageRect("frame")

    # Exit cleanly if you press q
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()