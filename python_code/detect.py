import cv2

w = 640
l = 480
deadzone = 5

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()

aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

capture = cv2.VideoCapture(1)

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
            print("DEADZONE")
        elif int(center) < w/2:
            print("left")
        else:
            print("right")

    # Show the result
    cv2.imshow('frame', frame)

    #if corners and corners[0] < w:
        #print("left")
    #else:
        #print("right")

    x, y, width, height = cv2.getWindowImageRect("frame")

    #cv2.line(frame, x, y, (255, 0, 0), 3)

    # Exit cleanly if you press q
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()