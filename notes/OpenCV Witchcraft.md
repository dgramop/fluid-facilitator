## The Plan.
**2 4x4 markers, 2 different ids, top and bottom of the cup.**

Position and range estimation must be derived from these markers.

The camera will rotate left and right but stay at a fixed vertical angle

## Important OpenCV Code

- [OpenCV ArUco Marker Detection Functions](https://docs.opencv.org/3.4/d9/d6a/group__aruco.html)
- [Perspective-n-Point (PnP) pose computation](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)
	- This is NOT related to ArUco markers, but may be useful
- [OpenCV Camera Calibration Tutorial](https://aliyasineser.medium.com/opencv-camera-calibration-e9a48bdd1844)

### Basic ArUco detection

#### 1) Load a predefined dictionary

```python
import cv2

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
```

Pre-defined dictionary can be one of [these.](https://docs.opencv.org/3.4/d9/d6a/group__aruco.html#gac84398a9ed9dd01306592dd616c2c975) In general, reducing the number of markers that the code is looking for allows for better error correction

From [OpenCV ArUco Detection Tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)

> In general, smaller dictionary sizes and larger marker sizes increase the inter-marker distance and vice versa. However, the detection of markers with larger sizes is more difficult due to the higher number of bits that need to be extracted from the image.

> For instance, if you need only 10 markers in your application, it is better to use a dictionary composed only of those 10 markers than using a dictionary composed of 1000 markers. The reason is that the dictionary composed of 10 markers will have a higher inter-marker distance and, thus, it will be more robust to errors.

#### 2) Instance a new [ArucoDetector](https://docs.opencv.org/4.x/d2/d1a/classcv_1_1aruco_1_1ArucoDetector.html)

```python
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
```

Not really sure what the parameters do but the defaults work just fine

#### 3) Start video capture

```python
camera_id = 0
capture = cv2.VideoCapture(camera_id)
```

#### 4) Read frames and run detection in a loop

```python
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

	# Show the result
    cv2.imshow('frame', frame)

	# Exit cleanly if you press q
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
	
```

The `corners` value is a list of 4-tuples of 2D vectors)
```
[
	[
		[541., 317.], # Corner 1 of marker 1
		[256., 328.], # Corner 2 of marker 1
		[235., 056.], # ...
		[510., 025.]
	],
	[
		[355., 367.], # Corner 1 of marker 2
        [139., 472.], # ...
        [065., 269.],
        [262., 182.]
	]
]
```


The `ids` value is a list of every detected marker ID in a frame, all markers have an ID number.
```plain
[4, 7]
```
