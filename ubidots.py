import time
import requests
import math
import random
import signal
import threading

# Import sensor-sensor
from gps import *
from heart_rate import *
from gyro import *
from ultrasonic import *
from led import *
from button import *

TOKEN = "BBFF-RT4uF3mKxwiiiZ9AIL6vyYClkSwvoz"  # Put your TOKEN here
DEVICE_LABEL = "ghuza-68"  # Put your device label here 
VARIABLE_LABEL_1 = "heart_rate"  # Put your first variable label here
VARIABLE_LABEL_2 = "oxygen"  # Put your first variable label here
VARIABLE_LABEL_3 = "gyro"  # Put your second variable label here
VARIABLE_LABEL_4 = "gps"  # Put your second variable label here
VARIABLE_LABEL_5 = "ultrasonic"

def build_payload(variable_1, variable_2, variable_3, variable_4, variable_5):
    # Creates two random values for sending data
    value_1 = get_hb2_spo2()[0] # Heartrate
    value_2 = get_hb2_spo2()[1] # Oxygen
    value_3 = get_orientation()
    value_5 = get_distance()

    # Creates a random gps coordinates
    print("GPS {}".format(get_gps_data()[0]))
    if(get_gps_data()[0] == 0.0):
        lat = random.randrange(34, 36, 1) + \
              random.randrange(1, 1000, 1) / 1000.0
        lng = random.randrange(-83, -87, -1) + \
              random.randrange(1, 1000, 1) / 1000.0
    else:
        lat = get_gps_data()[0]
        lng = get_gps_data()[1]
        
    # Data yang dikirim ke Ubidots dalam bentuk dictionary
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: value_3,
               variable_4: {"value": 1, "context": {"lat": lat, "lng": lng}},
               variable_5: value_5
    }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    # print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    #print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5)

    print("[Ubidots] Attemping to send data")
    post_request(payload)
    print("[Ubidots] finished")
    print("---------------------------------")


if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=main)
        t2 = threading.Thread(target=run_led)
        t3 = threading.Thread(target=emergency_button)
        
        # starting thread 1 & 2
        t1.start()
        t2.start()
        t3.start()
        
        # wait until thread 1 & 2 is completely executed
        t1.join()
        t2.join()
        t3.join()
     
        # both threads completely executed
        print("Done!")
        
    except KeyboardInterrupt:
        print("Turn off")
        GPIO.output(buzzer,GPIO.LOW)
        colorWipe(strip, Color(0,0,0), 10)
        GPIO.cleanup()
            
    finally:
        GPIO.cleanup()
        
#     while (True):
#         main()
#         run_led()