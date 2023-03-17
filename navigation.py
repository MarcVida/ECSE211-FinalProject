from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep
from color_detection import ColorDetector 

class Navigation:
    """Class for the navigation subsystem"""

    colordetector: ColorDetector = None
    motorL: Motor = None
    motorR: Motor = None
    isForward=True
    greenCount=0


    def __init__(self, motorPortL: int, motorPortR: int, colorDetector: ColorDetector, debug: bool=False) -> None:
        """Constructor for the Navigation class.

        Args:
            motorPortL (int): The port for the left motor.
            motorPortR (int): The port for the right motor.
            colorDetector (ColorDetector): The ColorDetector object.
        """
        self.motorL = Motor(motorPortL)
        self.motorR = Motor(motorPortR)
        self.colordetector = colorDetector
        self.debug=debug

    def navSequence(self):
        navSensor = EV3ColorSensor(None)

        """
        """
        while(True):
            color=self.colordetector.getNavSensorColor()

            if color=="BLUE":
                if(self.isForward):
                    self.turnLeft()
                else:
                    self.turnRight()


            elif color=="RED":
                if(self.isForward):
                    self.turnRight()
                else:
                    self.turnLeft()
            
            elif color=="GREEN":
                # Call position tracker and set new position
                self.positionTracker()

                #break
            elif color=="YELLOW":
                self.motorL.set_power(0)
                self.motorL.set_power(0)

                break
            else:
                if(self.isForward):
                    self.motorL.set_power(-30)
                    self.motorR.set_power(-30)
                else:
                    self.motorL.set_power(30)
                    self.motorR.set_power(30)
            sleep(0.1)

    def deliverySequence(self):
        pass

    def positionTracker(self):
        """Keeps track of position relative to the green lines on the map
        There are 6 total green lines
        """
        if(self.isForward):
            self.greenCount+=1
        else:
            self.greenCount-=1
        self.log("position is "+self.greenCount)


    def turnLeft(self):
        self.motorL.set_power(-30)
        self.motorR.set_power(0)

    def turnRight(self):
        self.motorL.set_power(0)
        self.motorR.set_power(-30)
    
    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)


if __name__ == '__main__':
    navigate=Navigation("A","B")
    try:
        navigate.navSequence()
    except BaseException:
        reset_brick()
        exit()