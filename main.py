import json
import os
import signal

import pyautogui
from PIL import Image
import pytesseract
import time
import matplotlib.pyplot as plt
import math

points_list = []

LATITUDE_CONSTANT = 111.32  # Approximate kilometers per degree latitude
LONGITUDE_CONSTANT = 111.32  # Approximate kilometers per degree longitude at the equator
FEET_TO_KILOMETERS = 0.0003048  # Conversion factor for feet to kilometers
KNOTS_TO_KILOMETERS_PER_HOUR = 1.852  # Conversion factor for knots to kilometers per hour

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude')
ax.set_title('Plane Coordinates')

current_latitude = 0
current_longitude = 0
elapsed_time = 0
last_alt = 0
last_heading = 0

while 1:
    try:
        stime = time.time()
        err = False
        screenshot = pyautogui.screenshot()
        heading = screenshot.crop((1660, 200, 1700, 260))
        heading_text = pytesseract.image_to_string(heading)
        try:
            heading_text = int(heading_text)
            last_heading = heading_text
        except:
            err = heading_text
            heading_text = last_heading

        screenshot = screenshot.crop((60, 1180, 500, 1520))
        extracted_text = pytesseract.image_to_string(screenshot)
        tt = str(extracted_text).split('\n')
        alt = 0
        spd = 0
        try:
            for data in tt:
                if 'Altitude:' in data:
                    alt = int(data.split(' ')[1])
                if 'Speed:' in data:
                    spd = int(data.split(' ')[1])
        except Exception as e:
            print(e)
            continue

        altitude_feet = alt
        speed_knots = spd
        vertical_speed_knots = 0
        heading_degrees = heading_text

        if speed_knots != 0:
            elapsed_time = time.time() - stime

            delta_latitude = (speed_knots * elapsed_time) / LATITUDE_CONSTANT
            delta_longitude = (speed_knots * elapsed_time) / (
                        LONGITUDE_CONSTANT * math.cos(math.radians(current_latitude)))

            heading_radians = math.radians(heading_degrees)

            delta_latitude = (speed_knots / LATITUDE_CONSTANT) + (
                    vertical_speed_knots * math.sin(heading_radians) / LATITUDE_CONSTANT)
            delta_longitude = (speed_knots / (LONGITUDE_CONSTANT * math.cos(math.radians(current_latitude))))

            new_latitude = current_latitude + delta_latitude
            new_longitude = current_longitude + delta_longitude

            change_in_latitude_due_to_altitude = (altitude_feet / LATITUDE_CONSTANT)
            new_latitude += change_in_latitude_due_to_altitude * math.cos(heading_radians)
            new_longitude += change_in_latitude_due_to_altitude * math.sin(heading_radians)

            # ax.scatter(new_longitude, new_latitude, altitude_feet, color='blue')
            # ax.plot([current_longitude, new_longitude], [current_latitude, new_latitude], [last_alt, altitude_feet],
            #         color='gray')

            # Update the current coordinates
            current_latitude = new_latitude
            current_longitude = new_longitude
            last_alt = alt

            # print([current_longitude, current_latitude, last_alt, spd, heading_text, err])
            points_list.append({'long': current_longitude, 'lat': current_latitude, 'altitude': last_alt, 'speed': spd,
                                'heading': heading_text, 'isHeadingError': err})
            # plt.pause(elapsed_time)

            # plt.plot(altitude_data)
            # plt.xlabel('Time')
            # plt.ylabel('Altitude')
            # plt.title('Altitude vs. Time')
            # plt.grid(True)
            # plt.pause(0.01)  # Pause for 1 second before updating the plot
            # plt.clf()  # Clear the current figure
    except KeyboardInterrupt as e:
        # print(points_list)
        with open(os.getcwd() + f'/flightdata-{time.time()}.json', 'w') as ff:
            ff.write(json.dumps(points_list))
        # before_sigint()
        pass