import cv2
import numpy as np
import time

# Define the color ranges for red and green in HSV color space
red_lower = np.array([0, 105, 0])
red_upper = np.array([19, 160, 245])
green_lower = np.array([75, 65, 0])
green_upper = np.array([100, 180, 255])

# Create a video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Minimum contour area threshold
min_contour_area = 1000

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply a Gaussian blur to the frame
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Create color masks for red and green
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Combine color masks
    combined_mask = cv2.bitwise_or(red_mask, green_mask)

    # Perform Canny edge detection on the combined mask
    edges = cv2.Canny(combined_mask, threshold1=30, threshold2=100)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [
        cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area
    ]

    # Draw bounding boxes and calculate center positions for filtered contours
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), -1)

    # Calculate the time it took to process the frame
    new_frame_time = time.time()

    # Calculate the frame rate
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Display the frame rate on terminal
    print("FPS: ", int(fps))

    # Display the frame
    cv2.imshow("Cuboid Box Detection", frame)

    # Check for the 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
