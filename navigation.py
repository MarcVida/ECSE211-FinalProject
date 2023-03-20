from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep
from color_detection import ColorDetector 

class Navigation:
    """Class for the navigation subsystem"""

    colordetector: ColorDetector = None
    motorL: Motor = None
    motorR: Motor = None
    isForward=True
    LAST_LOCATION = 6
    locations = [None for _ in range(0,LAST_LOCATION+1)]
    colors = ["","","","","",""]
    currColor: str = None

    currLocation = 0


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
                self.updatePosition()

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

    def updatePosition(self):
        """Keeps track of position relative to the green lines on the map
        There are 6 total green lines
        """
        if(self.isForward):
            self.currLocation+=1
        else:
            self.currLocation-=1
        self.log("Location is "+self.currLocation)


    def turnLeft(self):
        self.motorL.set_power(-30)
        self.motorR.set_power(0)

    def turnRight(self):
        self.motorL.set_power(0)
        self.motorR.set_power(-30)
    
    def goTowardsZone(self):
        """If it's going forward the delivery zone is to the right
        """
        if(self.isForward):
            self.motorL.set_power(30)
            sleep(0.75)
            self.motorL.set_power(0)
        
        else:
            self.motorR.set_power(30)
            sleep(0.75)
            self.motorR.set_power(0)

    def goTowardsPath(self):
        """Move back a little so it doesn't hit the cube. 
        Turn back to the road
        """
        self.motorL.set_power(30)
        self.motorR.set_power(30)
        sleep(0.25)
        self.motorL.set_power(0)
        self.motorR.set_power(0)
        if(self.isForward):
            self.motorL.set_power(-30)
            sleep(0.75)
            self.motorL.set_power(0)
        else:
            self.motorR.set_power(-30)
            sleep(0.75)
            self.motorL.set_power(0)
            
    def turnTowardsNextLocation(self):
        pass

    def getNextColor(self):
        pass

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