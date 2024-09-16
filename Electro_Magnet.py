# ELECTRO.py

import RPi.GPIO as GPIO
import time
from Config import ELECTRO_PINS

class ElectroMagnetControl:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_off()

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup(self.pin)

def activate_all_electro_magnets():
    # Initialiser les électro-aimants avec les pins du fichier config
    electro_magnets = {name: ElectroMagnetControl(pin) for name, pin in ELECTRO_PINS.items()}
    
    try:
        # Activer tous les électro-aimants
        for name, electro in electro_magnets.items():
            print(f"Activating electro-magnet: {name}")
            electro.turn_on()
        
        # Garder les électro-aimants activés pendant un certain temps (par exemple, 10 secondes)
        time.sleep(10)
    
    finally:
        # Éteindre tous les électro-aimants et nettoyer
        for electro in electro_magnets.values():
            electro.turn_off()
            electro.cleanup()

if __name__ == "__main__":
    activate_all_electro_magnets()
