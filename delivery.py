from utils.brick import Motor, TouchSensor
from time import sleep

def waitUntil(callback):
    while not callback():
        pass

class Delivery:

    deliveryMotor: Motor
    loadingTS: TouchSensor

    def __init__(self, deliveryPort: int, loadingPort: int, debug: bool) -> None:
            self.deliveryMotor = Motor(deliveryPort)
            self.loadingTS = TouchSensor(loadingPort)
            self.debug = debug

    def loadingSequence(self):
        # TODO: Implement this
        self.log("Loading...")
        waitUntil(self.isLoadingComplete)
        self.log("Loading complete.")

    def isLoadingComplete(self):
        return self.loadingTS.is_pressed()

    def deliverySequence(self):
        # TODO: Implement this
        self.log("Dropping cube...")
        waitUntil(self.isDeliveryComplete)
        self.log("Delivery complete.")

    def isDeliveryComplete(self):
        # TODO: Implement this
        return True

    def log(self, message: str):
        if self.debug: print(message)
    
if __name__ == "__main__":
    delivery = Delivery(0,0,True)
    delivery.loadingSequence()
    delivery.deliverySequence()