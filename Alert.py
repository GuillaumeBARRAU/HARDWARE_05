import smtplib
from email.mime.text import MIMEText
import time
from Config import EMAIL_CONFIG, BUTTON_PINS
from Button_Toggle import ButtonController
import RPi.GPIO as GPIO

class AlertSystem:
    def __init__(self, button_pin):
        GPIO.setmode(GPIO.BCM)
        self.button = ButtonController(button_pin)
        self.email_config = EMAIL_CONFIG
        self.button_was_pressed = False  # Pour suivre l'état précédent du bouton

    def send_alert(self):
        # Création du message d'alerte
        subject = "Alerte du Pilulier Connecté"
        body = "Une alerte a été déclenchée sur le pilulier connecté."
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config["sender_email"]
        msg['To'] = self.email_config["receiver_email"]

        # Envoyer l'email via SMTP
        try:
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["sender_email"], self.email_config["password"])
            server.sendmail(self.email_config["sender_email"], self.email_config["receiver_email"], msg.as_string())
            server.quit()
            print("Alerte envoyée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'alerte : {e}")

    def monitor_button(self):
        while True:
            if self.button.is_pressed():
                if not self.button_was_pressed:  # Si le bouton vient juste d'être pressé
                    self.send_alert()
                    self.button_was_pressed = True  # Marquer le bouton comme pressé
            else:
                self.button_was_pressed = False  # Réinitialiser l'état quand le bouton est relâché

            time.sleep(0.1)  # Évite de surcharger le CPU

    def run(self):
        try:
            self.monitor_button()
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        self.button.cleanup()
        GPIO.cleanup()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    # Récupérer les pins du fichier config
    BUTTON_PIN = BUTTON_PINS["ALERT"]  # Pin du bouton d'alerte dans config.py

    # Initialiser et lancer le système d'alerte
    alert_system = AlertSystem(BUTTON_PIN)
    alert_system.run()
