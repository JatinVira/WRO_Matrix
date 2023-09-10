import cv2
import numpy as np

# Define the color ranges for red and green in HSV color space
red_lower = np.array([0, 50, 50])
red_upper = np.array([10, 255, 255])
green_lower = np.array([45, 50, 50])
green_upper = np.array([75, 255, 255])

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

    # Combine color masks
    combined_mask = cv2.bitwise_or(red_mask, green_mask)

    # Perform Canny edge detection on the combined mask
    edges = cv2.Canny(combined_mask, threshold1=30, threshold2=100)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes and calculate center positions for contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Cuboid Box Detection', frame)

    # Check for the 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
