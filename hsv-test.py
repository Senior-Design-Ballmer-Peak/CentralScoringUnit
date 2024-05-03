import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a window to display the webcam feed
cv2.namedWindow('Webcam')

# Define a callback function to update the color range based on trackbar values
def update_range(value=0):
    global lower_range, upper_range

    # Get the trackbar values
    hue_lower = cv2.getTrackbarPos('Hue Lower', 'Webcam')
    hue_upper = cv2.getTrackbarPos('Hue Upper', 'Webcam')
    sat_lower = cv2.getTrackbarPos('Sat Lower', 'Webcam')
    sat_upper = cv2.getTrackbarPos('Sat Upper', 'Webcam')
    val_lower = cv2.getTrackbarPos('Val Lower', 'Webcam')
    val_upper = cv2.getTrackbarPos('Val Upper', 'Webcam')

    # Update the color ranges
    lower_range = np.array([hue_lower, sat_lower, val_lower])
    upper_range = np.array([hue_upper, sat_upper, val_upper])

    # Read the webcam frame
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply the color mask
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Display the result
    cv2.imshow('Webcam', cv2.bitwise_and(frame, frame, mask=mask))

# Create trackbars for adjusting the color range
cv2.createTrackbar('Hue Lower', 'Webcam', 0, 179, update_range)
cv2.createTrackbar('Hue Upper', 'Webcam', 179, 179, update_range)
cv2.createTrackbar('Sat Lower', 'Webcam', 0, 255, update_range)
cv2.createTrackbar('Sat Upper', 'Webcam', 255, 255, update_range)
cv2.createTrackbar('Val Lower', 'Webcam', 0, 255, update_range)
cv2.createTrackbar('Val Upper', 'Webcam', 255, 255, update_range)

# Call the update_range function to display the initial frame
update_range(0)

# Keep the window open until the user presses 'q'
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
