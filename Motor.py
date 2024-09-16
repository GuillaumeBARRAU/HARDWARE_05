# MOTOR.py

import RPi.GPIO as GPIO
import time
from Config import MOTOR_PINS

class MotorController:
    def __init__(self):
        # Récupérer les broches à partir du fichier config
        self.IN1 = MOTOR_PINS["IN1"]
        self.IN2 = MOTOR_PINS["IN2"]
        self.IN3 = MOTOR_PINS["IN3"]
        self.IN4 = MOTOR_PINS["IN4"]

        # Configurer les broches GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        # Séquence pour le moteur pas à pas (demi-pas)
        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
        ]

        # Définir le nombre de pas pour chaque position
        self.steps_per_position = [64, 64, 64, 64, 64, 64, 128]

    def set_step(self, step):
        GPIO.output(self.IN1, step[0])
        GPIO.output(self.IN2, step[1])
        GPIO.output(self.IN3, step[2])
        GPIO.output(self.IN4, step[3])

    def move_one_position(self, position):
        if position < 0 or position >= len(self.steps_per_position):
            raise ValueError("Invalid position index")
        steps = self.steps_per_position[position]
        for _ in range(steps):
            for step in self.step_sequence:
                self.set_step(step)
                time.sleep(0.01)  # Ajustez le délai selon la vitesse souhaitée
        time.sleep(5)  # Pause de 5 secondes après chaque position

    def loop_positions(self):
        position = 0
        while True:
            self.move_one_position(position)
            position = (position + 1) % len(self.steps_per_position)  # Passe à l'étape suivante, puis revient à 0 après 7

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    motor = MotorController()
    
    try:
        # Boucle sur les positions de manière infinie
        motor.loop_positions()
    except KeyboardInterrupt:
        print("Interruption du programme.")
    finally:
        motor.cleanup()
