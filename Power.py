from Button_Toggle import ButtonController
from Led_Toggle import LEDController
from Config import BUTTON_PINS, LED_PINS
import time
import RPi.GPIO as GPIO

class PowerControl:
    def __init__(self, button_pin, led_pin):
        GPIO.setmode(GPIO.BCM)
        self.button = ButtonController(button_pin)
        self.led = LEDController(led_pin)
        self.led_state = False  # LED éteinte au démarrage
        self.button_pressed = False  # Pour suivre l'état du bouton

    def toggle_led(self):
        # Vérifier si le bouton a été pressé
        if self.button.is_pressed():
            if not self.button_pressed:
                # Si le bouton était précédemment relâché et maintenant pressé
                self.led_state = not self.led_state  # Inverser l'état de la LED
                if self.led_state:
                    self.led.turn_on()
                else:
                    self.led.turn_off()
                self.button_pressed = True  # Marquer le bouton comme pressé
        else:
            self.button_pressed = False  # Réinitialiser lorsque le bouton est relâché

    def run(self):
        try:
            while True:
                self.toggle_led()
                time.sleep(0.1)  # Évite de surcharger le CPU
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        self.button.cleanup()
        self.led.cleanup()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)  # Assure que le mode BCM est utilisé

    # Récupérer les pins du fichier config
    BUTTON_PIN = BUTTON_PINS["POWER"]  # Pin du bouton POWER dans config.py
    LED_PIN = LED_PINS["POWER"]        # Pin de la LED POWER dans config.py

    power_control = PowerControl(BUTTON_PIN, LED_PIN)
    power_control.run()
