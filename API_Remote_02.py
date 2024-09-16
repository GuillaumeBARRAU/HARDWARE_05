from flask import Flask, jsonify
from Button_Toggle import ButtonController
from Led_Toggle import LEDController
from Led_Pulse import LEDPulseController
from Config import BUTTON_PINS, LED_PINS
import time
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)  # Initialisation de Flask

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

    def activate_remote(self):
        # Cette méthode sera appelée par l'API Flask pour activer la fonction remote
        print("Remote control activated via API")
        self.led.toggle()  # Exemple d'action à distance

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

# Initialisation de la classe RemoteControl
remote_control = RemoteControl(BUTTON_PINS["REMOTE"], LED_PINS["REMOTE"])

# Route Flask pour recevoir les requêtes de Symfony
@app.route('/pillbox/Remote', methods=['POST'])
def remote_control_api():
    # Appelle la méthode activate_remote() lorsque Symfony envoie une requête
    remote_control.activate_remote()
    return jsonify({"message": "Remote control activated successfully"}), 200

if __name__ == "__main__":
    # Lance le thread Flask pour écouter les requêtes à distance
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.start()

    # Continue à exécuter le programme Remote normalement
    remote_control.run()
