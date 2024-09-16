# LED_TOGGLE.py

import RPi.GPIO as GPIO

class LEDController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False  # État initial de la LED, éteinte

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def toggle(self):
        if self.state:
            self.turn_off()
        else:
            self.turn_on()

    def cleanup(self):
        GPIO.cleanup(self.pin)
