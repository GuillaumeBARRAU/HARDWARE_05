import RPi.GPIO as GPIO
import time

class LEDPulseController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False

    def pulse(self):
        self.state = not self.state
        GPIO.output(self.pin, GPIO.HIGH if self.state else GPIO.LOW)
        time.sleep(0.2)  # Durée de clignotement

    def cleanup(self):
        GPIO.cleanup(self.pin)
