import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import math

# Set up firebase
firebase_database_url = 'https://ssm-csu-default-rtdb.firebaseio.com/game_data'


def send_to_firebase(data):
    try:
        response = requests.patch(firebase_database_url + ".json", json=data)
        if response.status_code == 200:
            print("Data sent to firebase successfully")
        else:
            print("Failed to send data to firebase: ", response.text)
    except Exception as e:
        print("Error sending data to firebase: ", str(e))


def find_angle(point1, point2):
    vectorx = point2[0] - point1[0]
    vectory = point2[1] - point1[1]
    angle_rad = math.atan2(vectory, vectorx)
    angle_deg = rad_to_deg(angle_rad)
    # if angle_deg > 180:
    #     angle_deg -= 180
    return angle_deg


def rad_to_deg(radians):
    degrees = radians * (180 / math.pi)
    return degrees


# Open the webcam
videoPath = 'IMG_2661.MOV'
cam = cv2.VideoCapture(videoPath)

# Initialize variables
prev_time = time.time()
prev_x = 0
prev_y = 0
prev_speed = 0

# DUBUG GRAPH
plt.ion()
fig, ax = plt.subplots()
scatter = ax.scatter([], [])
ax.set_xlim(0, 1080)
ax.set_ylim(0, 1920)
ax.set_title('Puck Movement')
angle = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture frame")
        break

    x, y, w, h = 150, 55, 1000, 600

    cropped_frame = frame[y:y+h, x:x+w]

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for blue color in HSV
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([150, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area and circularity
    in_frame = False
    x_data = prev_x
    y_data = prev_y
    radius_data = 0
    speed = prev_speed

    largest_contour = None
    largest_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    if largest_contour is not None and largest_area > 5000:
        perimeter = cv2.arcLength(contour, True)
        print(largest_area)
        if perimeter != 0:
            circularity = 4 * np.pi * largest_area / (perimeter ** 2)

            if circularity > 0.3:
                # Draw a circle around the detected puck
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(cropped_frame, center, radius, (0, 255, 0), 2)
                in_frame = True
                x_data = x
                y_data = y
                radius_data = radius

    change_in_distance = math.sqrt((x_data - prev_x) ** 2 + (y_data - prev_y) ** 2)
    if x_data != prev_x and y_data != prev_y:
        angle = find_angle((prev_x, prev_y), (x_data, y_data))
    print(angle)
    prev_x = x_data
    prev_y = y_data

    current_time = time.time()
    time_difference = current_time - prev_time
    prev_time = current_time

    if radius_data != 0:
        speed = change_in_distance * (2 / radius_data) / time_difference
        prev_speed = speed

    data = {
        "in_frame": in_frame,
        "x": x_data,
        "y": y_data,
        "speed": speed,
        "angle": angle
    }

    send_to_firebase(data)

    scatter.set_offsets(np.c_[x_data, y_data])
    fig.canvas.draw_idle()
    plt.pause(0.01)

    # Display the frame with detected puck
    cv2.imshow("Air Hockey Puck Detection", cropped_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
