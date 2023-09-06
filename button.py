import RPi.GPIO as GPIO
from buzzer import *

BUTTON = 12
button_status = False

def button_changed(button):
    global button_status
    
    if GPIO.input(button) == GPIO.LOW:
        print("Button pressed.", button_status)
        button_status = not button_status
    else:
        print("Button released.", button_status)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_changed, bouncetime=10)

def emergency_button():
    while True:
        if(button_status == True):
            buzzer_on()
        else:
            buzzer_off()
