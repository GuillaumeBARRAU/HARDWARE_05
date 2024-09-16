import RPi.GPIO as GPIO
import time

class ButtonController:
    def __init__(self, pin, press_time=0.1):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.press_time = press_time  # Temps en secondes pour considérer un appui comme valide
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        start_time = time.time()
        while GPIO.input(self.pin) == GPIO.LOW:  # Le bouton est enfoncé
            if time.time() - start_time >= self.press_time:
                return True
            time.sleep(0.01)  # Petite pause pour éviter une surcharge CPU
        return False

    def cleanup(self):
        GPIO.cleanup(self.pin)
