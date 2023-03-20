from utils.brick import Motor, TouchSensor, reset_brick
from utils.sound import Sound
from time import sleep

def waitUntil(callback):
    while not callback():
        pass

class Delivery:
    """Class for the delivery subsystem."""

    deliveryMotor: Motor = None
    loadingTS: TouchSensor = None
    SOUND1: Sound = None
    SOUND2: Sound = None

    def __init__(self, deliveryPort: int, loadingPort: int, debug: bool = False) -> None:
        """Constructor for the Delivery class.

        Args:
            deliveryPort (int): The port for the delivery motor.
            loadingPort (int): The port for the loading touch sensor.
            debug (bool, optional): Sets whether the object is in debug mode. Defaults to False.
        """
        self.deliveryMotor = Motor(deliveryPort)
        self.loadingTS = TouchSensor(loadingPort)
        self.SOUND1 = Sound(duration=0.5, pitch="G5", volume=80)
        self.SOUND2 = Sound(duration=0.5, pitch="C6", volume=80)
        self.debug = debug

    def loadingSequence(self):
        """Starts the loading sequence: Wait for the user to load the cubes.
        """
        self.SOUND1.play()
        self.log("Loading...")
        waitUntil(self.isLoadingComplete)
        self.SOUND2.play()
        self.log("Loading complete.")
        self.SOUND2.wait_done()

    def isLoadingComplete(self):
        return self.loadingTS.is_pressed()

    def deliverySequence(self):
        """Starts the delivery sequence: Drop a cube.
        """
        self.log("Dropping cube...")
        self.deliveryMotor.set_limits(40)
        self.deliveryMotor.set_position_relative(-90)
        sleep(1)
        self.deliveryMotor.set_position_relative(-80)
        sleep(1)
        self.deliveryMotor.set_power(0)
        self.log("Delivery complete.")

    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)
    
if __name__ == "__main__":
    delivery = Delivery(1, 2, debug=True)
    while(True):
        try:
            delivery.loadingSequence()
            delivery.deliverySequence()
        except BaseException:
            reset_brick()
            exit()