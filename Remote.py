from Button_Toggle import ButtonController
from Led_Toggle import LEDController
from Led_Pulse import LEDPulseController
from Config import BUTTON_PINS, LED_PINS
import time
import threading
import RPi.GPIO as GPIO

class RemoteControl:
    def __init__(self, button_pin, led_pin):
        GPIO.setmode(GPIO.BCM)
        self.button = ButtonController(button_pin)
        self.led = LEDController(led_pin)
        self.led_pulse = LEDPulseController(led_pin)  # Utilise la même LED pour le clignotement
        self.running = True

    def handle_button_press(self):
        while self.running:
            if self.button.is_pressed():
                self.led.toggle()
                time.sleep(0.3)  # Debounce: éviter les multiples basculements rapides
            time.sleep(0.1)  # Évite de surcharger le CPU

    def handle_button_hold(self):
        while self.running:
            if self.button.is_pressed():  # Si le bouton est maintenu enfoncé
                self.led_pulse.pulse()
            time.sleep(0.1)  # Évite de surcharger le CPU

    def run(self):
        try:
            button_thread = threading.Thread(target=self.handle_button_press)
            hold_thread = threading.Thread(target=self.handle_button_hold)
            button_thread.start()
            hold_thread.start()
            button_thread.join()
            hold_thread.join()
        except KeyboardInterrupt:
            self.running = False
            button_thread.join()
            hold_thread.join()
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    remote_control = RemoteControl(BUTTON_PINS["REMOTE"], LED_PINS["REMOTE"])
    remote_control.run()
