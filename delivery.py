from utils.brick import Motor, TouchSensor

class Delivery:

    deliveryMotor: Motor
    loadingTS: TouchSensor

    def __init__(self, deliveryPort: int, loadingPort: int) -> None:
            self.deliveryMotor = Motor(deliveryPort)
            self.loadingTS = TouchSensor(loadingPort)

    def loadingSequence():
        pass

    def isLoadingComplete():
        pass

    def deliverySequence():
        pass

    def isDeliveryComplete():
        pass
    
