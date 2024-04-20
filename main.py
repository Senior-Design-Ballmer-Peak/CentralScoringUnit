import cv2
import numpy as np
import requests

# Set up firebase
firebase_database_url = 'https://ssm-csu-default-rtdb.firebaseio.com/'

def send_to_firebase(data):
	try:
		response = requests.patch(firebase_database_url + ".json", json=data)
		if response.status_code == 200:
			print("Data sent to firebase successfully")
		else:
			print("Failed to send data to firebase: ", response.text)
	except Exception as e:
		print("Error sending data to firebase: ", str(e))

# Open the webcam
cam = cv2.VideoCapture(0)

while True:
	ret, frame = cam.read()
	if not ret:
		print("Failed to capture frame")
		break
      
	# Convert BGR image to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
	# Define lower and upper bounds for blue color in HSV
	lower_blue = np.array([100, 50, 50])
	upper_blue = np.array([130, 255, 255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# Find contours in the masked image
	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Filter contours by area and circularity
	in_frame = False
	x_data = 0
	y_data = 0
	for contour in contours:
		area = cv2.contourArea(contour)
		perimeter = cv2.arcLength(contour, True)
		if perimeter != 0:
			circularity = 4 * np.pi * area / (perimeter ** 2)
			
			# You may need to adjust the circularity threshold based on your puck size and shape
			if circularity > 0.7:
				# Draw a circle around the detected puck
				(x, y), radius = cv2.minEnclosingCircle(contour)
				center = (int(x), int(y))
				radius = int(radius)
				cv2.circle(frame, center, radius, (0, 255, 0), 2)
				in_frame = True
				x_data = x
				y_data = y
	data = {
		"in_frame": in_frame,
		"x": x_data,
		"y": y_data
	}
	send_to_firebase(data)

	# Display the frame with detected puck
	# cv2.imshow("Air Hockey Puck Detection", frame)
    
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

# Release the webcam and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
