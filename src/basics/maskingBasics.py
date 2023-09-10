"""
Code to try out Color Masking in OpenCV
And draw a bounding box around the detected object
"""
import cv2
from PIL import Image
import numpy as np

# Create a capture method and read from the webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of yellow color in HSV
    lowerLimit = np.array([16, 110, 206])
    upperLimit = np.array([25, 236, 255])

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow("mask", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
