from utils.brick import Motor, TouchSensor, reset_brick
from utils.sound import Sound
from time import sleep

class Delivery:
    """Class for the delivery subsystem."""

    ################# CONSTANTS #################
    
    MOVEMENT_DEG = 90
    MOVEMENT_TIME = 1
    MOVEMENT_LIMIT = 65

    ################# VARIABLES #################

    deliveryMotor: Motor = None
    touchSensor: TouchSensor = None
    sound1: Sound = None
    sound2: Sound = None

    ################## METHODS ##################

    def __init__(self, deliveryMotorPort: int, touchSensorPort: int, debug: bool = False) -> None:
        """Constructor for the Delivery class.

        Args:
            deliveryPort (int): The port for the delivery motor.
            loadingPort (int): The port for the loading touch sensor.
            debug (bool, optional): Sets whether the object is in debug mode. Defaults to False.
        """
        self.deliveryMotor = Motor(deliveryMotorPort)
        self.touchSensor = TouchSensor(touchSensorPort)
        self.sound1 = Sound(duration=0.5, pitch="G5", volume=80)
        self.sound2 = Sound(duration=0.5, pitch="C6", volume=80)
        self.debug = debug

    def loadingSequence(self):
        """Starts the loading sequence: Wait for the user to load the cubes.
        """
        self.sound1.play()
        self.log("Loading...")
        while not self.touchSensor.is_pressed():
            pass
        self.sound2.play()
        self.log("Loading complete.")
        self.sound2.wait_done()

    def deliverySequence(self):
        """Starts the delivery sequence: Drop a cube.
        """
        self.log("Dropping cube...")
        self.deliveryMotor.set_limits(self.MOVEMENT_LIMIT)
        self.deliveryMotor.set_position_relative(-self.MOVEMENT_DEG)
        sleep(self.MOVEMENT_TIME)
        self.deliveryMotor.set_position_relative(self.MOVEMENT_DEG)
        sleep(self.MOVEMENT_TIME)
        self.deliveryMotor.set_power(0)
        self.log("Delivery complete.")

    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)
    
if __name__ == "__main__":
    delivery = Delivery("D", 2, debug=True)
    while(True):
        try:
            delivery.loadingSequence()
            delivery.deliverySequence()
        except BaseException:
            reset_brick()
            exit()