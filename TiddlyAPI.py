__author__ = 'alexgray'

import RPi.GPIO as GPIO
from RPIO import PWM
import time
import sys

## set which pins are operating the motors, the line sensor and LED's
## CONSTANTS
left_motor = 17
right_motor = 27
camera_servo = 22
pen_servo = 9
line_sensor = 23
led_one = 2
led_two = 3
led_three = 4

## Variables for smooth servo rotation
target_left = 1520
target_right = 1520
last_tick = 0

count = 0
led_count = 0


class TiddlyBot():
    
    def __init__(self):
        ## Setup GPIO for reading the line sensor and LED's
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(line_sensor, GPIO.IN)
        GPIO.setup(led_one, GPIO.OUT)
        GPIO.setup(led_two, GPIO.OUT)
        GPIO.setup(led_three, GPIO.OUT)
        ## Default LED's to off
        GPIO.output(led_one, False)
        GPIO.output(led_two, False)
        GPIO.output(led_three, False)
        ## Set up PWM for servos
        servo = PWM.Servo()
    
    def update(self):
        global current_left, current_right
        current_left = self.update_servos(current_left, target_left, left_motor)
        current_right = self.update_servos(current_right, target_right, right_motor)

        ## Logic for TiddlyBot
    @staticmethod
    def set_target_speed(left, right):  # Set target speed to achieve
        global target_left, target_right
        target_left = 1520 - int(left)
        target_right = 1520 + int(right)

    def update_servos(self, current, target, motor):  # Set servos toward target at  fixed rate
        direction = int(target - current)
        if current == target:
            return current
        direction = self.normalise(direction)
        current = self.smooth_movement_servos(motor, current, direction)
        return int(current)

    @staticmethod
    def normalise(direction):  # Take different in target and current to get direction
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        else:
            direction = 0
        return direction

        ## Wheel servo functions
    def turn_movement_servos(self, left_speed, right_speed):  # Hard setting of left and right wheel servos
        self.servo.set_servo(left_motor, 1520 + (-1 * int(left_speed)))
        self.servo.set_servo(right_motor, 1520 + (1 * int(right_speed)))

    def smooth_movement_servos(self, motor, pwm, direction):  # Set a servo with small increment (direction), return pwm
        pwm += int(direction) * 10
        self.servo.set_servo(motor, pwm)
        return pwm

        ## Line following functions
    @staticmethod
    def check_on_line():  # Check if TiddlyBot is on a line or not
        if GPIO.input(line_sensor) == GPIO.LOW:
            on_line = True
        else:
            on_line = False
        return on_line

    def line_following(self):  # Basic line following algorithm
        if self.check_on_line():
            self.turn_movement_servos(100, 40)
        else:
            self.turn_movement_servos(40, 100)
        time.sleep(0.1)

        ## Led functions
    @staticmethod
    def toggle_led(led_on, led_pin):
        if led_on:
            GPIO.output(led_pin, False)
            led_on = not led_on
        else:
            GPIO.output(led_pin, True)
            led_on = not led_on
        return led_on

    def led_display(self, led_counter):
        if led_counter == 1:
            self.set_led(1, 0, 0)  # red
        elif led_counter == 2:
            self.set_led(0, 1, 0)  # green
        elif led_counter == 3:
            self.set_led(0, 0, 1)   # blue
        elif led_counter == 4:
            self.set_led(1, 1, 0)   # yellow
        elif led_counter == 5:
            self.set_led(1, 0, 1)  # indigo
        elif led_counter == 6:
            self.set_led(0, 1, 1)  # cyan
        elif led_counter == 6:
            self.set_led(1, 1, 1)  # white
        elif led_counter == 6:
            self.set_led(0, 0, 0)  # off

    @staticmethod
    def set_led(one, two, three):
        GPIO.output(led_one, one)
        GPIO.output(led_two, two)
        GPIO.output(led_three, three)

        ## Extra movement servo functions
    def pen_movement(self, position):  # Move pen servo up or down, takes a string
        if position == "up":
            self.servo.set_servo(pen_servo, 2200)
        elif position == "down":
            self.servo.set_servo(pen_servo, 600)

    def camera_movement(self, direction, step, state):  # Move camera to different positions in steps
        if direction is "up":
            if (state - step) > 700:
                state -= step
            elif (state - step) <= 700:
                state = 700
        elif direction is "down":
            if (state + step) < 2400:
                state += step
            elif (state + step) >= 2400:
                state = 2400
        self.servo.set_servo(camera_servo, state)
        return state

        ## Time functions
    @staticmethod
    def get_time():  #
        return time.time() * 1000

    def get_delta(self):  #
        global last_tick
        current_time = self.get_time()
        delta = (int(current_time - last_tick))
        last_tick = self.get_time()
        return delta