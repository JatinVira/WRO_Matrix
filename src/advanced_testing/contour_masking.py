import cv2
import numpy as np


# Define the color ranges for red in HSV color space
red_lower = np.array([0, 116, 88])
red_upper = np.array([179, 255, 255])

# Define the color ranges for green in HSV color space
green_lower = np.array([23, 45, 13])
green_upper = np.array([72, 195, 255])

# Create a video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create color masks for red and green
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours in the color masks
    red_contours, _ = cv2.findContours(
        red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    green_contours, _ = cv2.findContours(
        green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw bounding boxes and calculate center positions for red contours
    for contour in red_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)

    # Draw bounding boxes and calculate center positions for green contours
    for contour in green_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow("Cuboid Box Detection", frame)

    # Check for the 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
