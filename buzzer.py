import RPi.GPIO as GPIO
from time import sleep

#Disable warnings (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Set buzzer - pin 23 as output
buzzer=23
GPIO.setup(buzzer,GPIO.OUT)

#Run forever loop
def buzzer_on():
    GPIO.output(buzzer,GPIO.HIGH)
    print ("Beep")
    sleep(1) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    print ("No Beep")
    sleep(0.5)
    
def buzzer_off():
    GPIO.output(buzzer,GPIO.LOW)