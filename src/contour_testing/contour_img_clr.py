"""
Code specifically to preporcess the image for contour detection
using color masking on image, creating a binary image
and then draw a bounding box around the detected object
approach failed
"""

import cv2
import numpy as np

# Read the image from the disk
color_img = cv2.imread("Images/red_box_simple_2.jpeg", 1)
# mask image according to hsv color range
hsv_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

# define range of red color in HSV
lower_red = np.array([0, 20, 35])
upper_red = np.array([180, 220, 255])
mask = cv2.inRange(hsv_img, lower_red, upper_red)
mask_ = cv2.bitwise_not(mask)


# Find the contours from the binary image
contours, hierachy = cv2.findContours(
    mask_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
)

# Draw all the contours on the original image
cv2.drawContours(color_img, contours, -1, (255, 0, 0), 2)

# Display the total number of contours found.
print("Number of contours found = {}".format(len(contours)))

cv2.imshow("Original Image", color_img)
cv2.imshow("Mask", mask)
cv2.imshow("Mask_", mask_)
cv2.waitKey(0)

cv2.destroyAllWindows()
