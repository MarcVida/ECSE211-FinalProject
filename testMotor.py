from utils.brick import Motor, TouchSensor, reset_brick
from utils.sound import Sound
from time import sleep

POWER = 20
DELAY = 4

motor = Motor('A')
motor.set_power(POWER)
sleep(DELAY)
motor.set_power(-POWER)
sleep(DELAY)
motor.set_power(0)