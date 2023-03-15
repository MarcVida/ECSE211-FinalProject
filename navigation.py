from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor
from time import sleep
from color_detection import ColorDetector 

class Navigation:
    """Class for the navigation subsystem"""

    colordetector: ColorDetector = None
    motorL: Motor = None
    motorR: Motor = None

    def __init__(self, motorPortL: int, motorPortR: int, colorDetector: ColorDetector) -> None:
        """Constructor for the Navigation class.

        Args:
            motorPortL (int): The port for the left motor.
            motorPortR (int): The port for the right motor.
            colorDetector (ColorDetector): The ColorDetector object.
        """
        self.motorL = Motor(motorPortL)
        self.motorR = Motor(motorPortR)
        self.colordetector = colorDetector

    def navSequence(self):
        navSensor = EV3ColorSensor(None)

        while(True):
            color=self.colordetector.getNavSensorColor()

            if color=="BLUE":
                self.motorL.set_power(30)
                self.motorR.set_power(0)

            elif color=="RED":
                self.motorL.set_power(0)
                self.motorR.set_power(30)
            
            elif color=="GREEN":

                # Call position tracker and set new position

                break
            elif color=="YELLOW":

                break
            else:
                self.motorL.set_power(30)
                self.motorR.set_power(30)
            sleep(0.1)

    def deliverySequence(self):
        pass

    def positionTracker(self):
        greenCount=0
        pass


if __name__ == '__main__':
    navigate=Navigation("A","B")
    navigate.navSequence()
    exit()