import cv2
import numpy as np
from calibration import load_coefficients

### INCOMPLETE ###
# This estimates a point in 3D space using known marker sizes in millimeters

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

camera_id = 1
capture = cv2.VideoCapture(camera_id)

c_mat, d_mat = load_coefficients('./cam_calibration2.dat')

square_size = 24.0 # mm

square_obj = np.array(
    [
        [ -1 * square_size / 2, 1 * square_size / 2, 0 ],
        [ 1 * square_size / 2, 1 * square_size / 2, 0 ],
        [ 1 * square_size / 2, -1 * square_size / 2, 0 ],
        [ -1 * square_size / 2, -1 * square_size / 2, 0 ],
    ]
)

square_obj = cv2.Mat(square_obj)

while True:
    # read() returns false for ret if a frame cant be captured for some reason
    ret, frame = capture.read()

    if not ret:
        break

    # Detect them squares
    corners, ids, rejected_points = aruco_detector.detectMarkers(frame)

    # Draw them if there is at least one
    if len(corners) > 0:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    for marker in corners:
        ret, rvec, tvec = cv2.solvePnP(
            square_obj,
            corners[0],
            c_mat,
            d_mat,
            None,
            None,
            flags=cv2.SOLVEPNP_IPPE_SQUARE
        )

    # Show the result
    cv2.imshow('frame', frame)

    # Exit cleanly if you press q
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
    