"""
Code specifically to pre process the frames from video for contour detection using
Color image, gaussian blur, and Canny Edge detction
and then draw a bounding box around the same
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    color_img = frame
    blur_img = cv2.GaussianBlur(color_img, (5, 5), 0)

    edges = cv2.Canny(blur_img, 50, 160)

    contours, hierachy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    cv2.drawContours(color_img, contours, -1, (255, 0, 0), 5)

    # Display the total number of contours found.
    print("Number of contours found = {}".format(len(contours)))

    cv2.imshow("Color_Img", color_img)
    cv2.imshow("Edge", edges)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
