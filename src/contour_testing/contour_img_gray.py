"""
Code specifically to preporcess the image for contour detection
using grayscale image and binary thresholding
and then draw a bounding box around the detected object
"""

import cv2
import numpy as np

# Read the image from the disk
color_img = cv2.imread("Images/red_box_simple_2.jpeg", 1)
gray_img = cv2.imread("Images/red_box_simple_2.jpeg", 0)
gray_inverted = cv2.bitwise_not(gray_img)
_, binary_img = cv2.threshold(gray_inverted, 140, 255, cv2.THRESH_BINARY)

# Find the contours from the binary image
contours, hierachy = cv2.findContours(
    binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
)

# Draw all the contours on the original image
cv2.drawContours(color_img, contours, -1, (255, 0, 0), 2)

# Display the total number of contours found.
print("Number of contours found = {}".format(len(contours)))

cv2.imshow("Original Image", color_img)
# cv2.imshow("Gray Image", gray_img)
# cv2.imshow("Gray Inverted", gray_inverted)
# cv2.imshow("Binary", binary_img)
cv2.waitKey(0)

cv2.destroyAllWindows()
