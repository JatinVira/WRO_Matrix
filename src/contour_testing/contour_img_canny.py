"""
Code specifically to pre process the images for contour detection using
Color image, gaussian blur, and Canny Edge detction
and then draw a bounding box around the same
"""

import cv2
import numpy as np

# Open an image
color_img = cv2.imread("Images/red_box_simple_2.jpeg", 1)
blur_img = cv2.GaussianBlur(color_img, (5, 5), 0)

edges = cv2.Canny(blur_img, 50, 160)
contours, hierachy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Display the total number of contours found.
print("Number of contours found = {}".format(len(contours)))

# Draw all the contours found
cv2.drawContours(color_img, contours, -1, (255, 0, 0), 5)

# Draw bounding box around the contours
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Color_Img", color_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
