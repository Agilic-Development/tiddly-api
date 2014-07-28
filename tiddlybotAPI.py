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


class TiddlyBot:
    
    
    def __init__(self):
        pass
    
    
    def __del__(self):
        self.set_led(0,0,0)
        self.turn_movement_servos(0, 0)
        PWM.cleanup()
        time.sleep(0.5)
        sys.exit()
    
    
    def test():
        servo = PWM.Servo()
        servo.set_servo(left_motor, 1200)
        
    
    def update():
        ## every loop, execute this logic
        count += 1
        if count >= 10:
            current_left = update_servos(current_left, target_left, left_motor)
            current_right = update_servos(current_right, target_right, right_motor)
            if led_light_show:  # Logic for led light show
                if int(round(led_counter)) == 6: 
                    led_counter = 0
                led_counter +=0.2
                led_display(int(round(led_counter)))
            count = 0


    def old_main(): 
        global last_tick
        count = 0
        led_1_on = False
        led_2_on = False
        led_3_on = False
        led_light_show = False
        led_counter = 0
        last_tick = get_time()
        current_left = 1520
        current_right = 1520
        ##default camera position
        state = 1500
        ##camera step difference
        step = 100
        

        ## Logic for TiddlyBot


    def set_target_speed(left, right):  # Set target speed to achieve
        global target_left, target_right
        target_left = 1520 - int(left)
        target_right = 1520 + int(right)


    def update_servos(current, target, motor):  # Set servos toward target at  fixed rate
        direction = int(target - current)
        if current == target:
            return current
        direction = direction_correcting(direction)
        current = smooth_movement_servos(motor, current, direction)
        return int(current)


    def direction_correcting(direction):  # Take different in target and current to get direction
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        else:
            direction = 0
        return int(direction)


        ## Wheel servo functions


    def turn_movement_servos(self, left_speed, right_speed):  # Hard setting of left and right wheel servos
        servo.set_servo(left_motor, 1520 + (-1 * int(left_speed)))
        servo.set_servo(right_motor, 1520 + (1 * int(right_speed)))


    def smooth_movement_servos(motor, pwm, direction):  # Set a servo with small increment (direction), return new pwm
        pwm += int(direction) * 10
        servo.set_servo(motor, int(pwm))
        return int(pwm)


        ## Line following functions


    def check_on_line():  # Check if TiddlyBot is on a line or not
        if GPIO.input(line_sensor) == GPIO.LOW:
            on_line = True
        else:
            on_line = False
        return on_line


    def line_following():  # Basic line following algorithm
        if check_on_line():
            turn_movement_servos(100, 40)
        else:
            turn_movement_servos(40, 100)
        time.sleep(0.1)


        ## Led functions
    def toggle_led(led_on, led_pin):
        if led_on:
            GPIO.output(led_pin, False)
            led_on = not led_on
        else:
            GPIO.output(led_pin, True)
            led_on = not led_on
        return led_on


    def led_display(led_counter):
        if led_counter == 1:
            set_led(1,0,0)  # red
        elif led_counter == 2:
            set_led(0,1,0)  # green
        elif led_counter == 3:
            set_led(0,0,1)   # blue
        elif led_counter == 4:
            set_led(1,1,0)   # yellow
        elif led_counter == 5:
            set_led(1,0,1)  # indigo
        elif led_counter == 6:
            set_led(0,1,1)  # cyan
        elif led_counter == 6:
            set_led(1,1,1)  # white
        elif led_counter == 6:
            set_led(0,0,0)  # off
    
    
    def set_led(one, two, three):
        GPIO.output(led_one, one)
        GPIO.output(led_two, two)
        GPIO.output(led_three, three)


        ## Extra movement servo functions


    def pen_movement(position):  # Move pen servo up or down, takes a string
        if position == "up":
            servo.set_servo(pen_servo, 2200)
        elif position == "down":
            servo.set_servo(pen_servo, 600)


    def camera_movement(direction, step, state):  # Move camera to different positions in steps
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
        servo.set_servo(camera_servo, state)
        return state


        ## Time functions


    def get_time():  #
        return time.time() * 1000


    def get_delta():  #
        global last_tick
        current_time = get_time()
        delta = (int(current_time - last_tick))
        last_tick = get_time()
        return delta
        
        
    def disconect(self):
        self.set_led(0,0,0)
        self.turn_movement_servos(0, 0)
        PWM.cleanup()
        time.sleep(0.5)
        sys.exit()
        