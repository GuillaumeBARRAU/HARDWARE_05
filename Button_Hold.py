import RPi.GPIO as GPIO
import time

class HoldButtonController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_held(self):
        start_time = time.time()
        while GPIO.input(self.pin) == GPIO.LOW:
            if time.time() - start_time > 5:  # 1 seconde pour considérer comme maintenu
                return True
        return False

    def cleanup(self):
        GPIO.cleanup(self.pin)
