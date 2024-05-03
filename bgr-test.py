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
    blue_lower = cv2.getTrackbarPos('Blue Lower', 'Webcam')
    blue_upper = cv2.getTrackbarPos('Blue Upper', 'Webcam')
    green_lower = cv2.getTrackbarPos('Green Lower', 'Webcam')
    green_upper = cv2.getTrackbarPos('Green Upper', 'Webcam')
    red_lower = cv2.getTrackbarPos('Red Lower', 'Webcam')
    red_upper = cv2.getTrackbarPos('Red Upper', 'Webcam')

    # Update the color ranges
    lower_range = np.array([blue_lower, green_lower, red_lower])
    upper_range = np.array([blue_upper, green_upper, red_upper])

    # Read the webcam frame
    ret, frame = cap.read()

    # Apply the color mask
    mask = cv2.inRange(frame, lower_range, upper_range)

    # Display the result
    cv2.imshow('Webcam', cv2.bitwise_and(frame, frame, mask=mask))

# Create trackbars for adjusting the color range
cv2.createTrackbar('Blue Lower', 'Webcam', 0, 255, update_range)
cv2.createTrackbar('Blue Upper', 'Webcam', 255, 255, update_range)
cv2.createTrackbar('Green Lower', 'Webcam', 0, 255, update_range)
cv2.createTrackbar('Green Upper', 'Webcam', 255, 255, update_range)
cv2.createTrackbar('Red Lower', 'Webcam', 0, 255, update_range)
cv2.createTrackbar('Red Upper', 'Webcam', 255, 255, update_range)

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
