from utils.brick import Motor, TouchSensor
from time import sleep

def waitUntil(callback):
    while not callback():
        pass

class Delivery:
    """Class for the delivery subsystem."""

    deliveryMotor: Motor = None
    loadingTS: TouchSensor = None

    def __init__(self, deliveryPort: int, loadingPort: int, debug: bool = False) -> None:
        """Constructor for the Delivery class.

        Args:
            deliveryPort (int): The port for the delivery motor.
            loadingPort (int): The port for the loading touch sensor.
            debug (bool, optional): Sets whether the object is in debug mode. Defaults to False.
        """
        self.deliveryMotor = Motor(deliveryPort)
        self.loadingTS = TouchSensor(loadingPort)
        self.debug = debug

    def loadingSequence(self):
        """Starts the loading sequence: Wait for the user to load the cubes.
        """
        self.log("Loading...")
        waitUntil(self.isLoadingComplete)
        self.log("Loading complete.")

    def isLoadingComplete(self):
        return self.loadingTS.is_pressed()

    def deliverySequence(self):
        """Starts the delivery sequence: Drop a cube.
        """
        self.log("Dropping cube...")
        self.deliveryMotor.set_limits(50)
        self.deliveryMotor.set_position_relative(80)
        #waitUntil(self.isDeliveryComplete)
        sleep(4)
        self.deliveryMotor.set_position_relative(-80)
        sleep(3)
        self.deliveryMotor.set_power(0)
        self.log("Delivery complete.")

    def isDeliveryComplete(self):
        # TODO: Implement this
        return True

    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)
    
if __name__ == "__main__":
    delivery = Delivery(1,2,True)
    delivery.loadingSequence()
    delivery.deliverySequence()