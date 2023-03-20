from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep, time
from color_detection import ColorDetector 

class Navigation:
    """Class for the navigation subsystem"""

    TURN_180_TIME = 5

    colordetector: ColorDetector = None
    motorL: Motor = None
    motorR: Motor = None
    isForward = True
    LAST_LOCATION = 6
    colorsInMap = [None] * (LAST_LOCATION + 1)
    colorsToDeliver = ["PURPLE","BLUE","GREEN", "YELLOW", "ORANGE"]
    nextColor = "RED"
    currLocation = 0
    timer = 0


    def __init__(self, motorPortL: int, motorPortR: int, colorDetectorPort: int, debug: bool=False) -> None:
        """Constructor for the Navigation class.

        Args:
            motorPortL (int): The port for the left motor.
            motorPortR (int): The port for the right motor.
            colorDetector (ColorDetector): The ColorDetector object.
        """
        self.motorL = Motor(motorPortL)
        self.motorR = Motor(motorPortR)
        self.colordetector = ColorDetector(colorDetectorPort)
        self.debug=debug

    def navSequence(self):
        self.resetTimer()
        while(True):
            color=self.colordetector.getNavSensorColor()

            if color=="BLUE":
                self.log("BLUE")
                if(self.isForward):
                    self.turnLeft()
                else:
                    self.turnRight()

            elif color=="RED":
                self.log("RED")
                if(self.isForward):
                    self.turnRight()
                else:
                    self.turnLeft()

            elif color=="GREEN" and time() > self.timer:
                # Update location, return DELIVERY flag if correct location
                # If DELIVERY flag is returned, the main module must call goTowardsPath() and turnTowardsNextLocation()
                self.stop()
                self.updateLocation()
                self.log("GREEN")
                self.log(f"current location: index={self.currLocation}, color={self.colorsInMap[self.currLocation]}")
                if not self.colorsInMap[self.currLocation]:
                    self.goTowardsZone()
                    zoneColor = self.colordetector.getNavSensorColor()
                    self.colorsInMap[self.currLocation] = zoneColor
                    self.log(f"detected color: {zoneColor}")
                    self.log(f"colors in map update:", self.colorsInMap)
                    if zoneColor == self.nextColor:
                        return "DELIVERY"
                    self.goTowardsPath()
                elif self.colorsInMap[self.currLocation] == self.nextColor:
                    self.goTowardsZone()
                    return "DELIVERY"
                self.log("no delivery")
                self.resetTimer()

            elif color=="YELLOW" and time() > self.timer:
                # Return LOADING flag
                self.stop()
                self.updateLocation()
                self.log(f"current location index: {self.currLocation}")
                self.rotateForward()
                self.isForward = True
                self.colorsToDeliver = ["YELLOW","PURPLE","BLUE","GREEN", "YELLOW", "ORANGE"]
                self.nextColor = "RED"
                return "LOADING"
            
            else:
                self.goForward()

            sleep(0.1)

    def updateLocation(self):
        """Keeps track of position relative to the yellow/green lines on the map
        There are 7 total yellow/green lines
        """
        if(self.isForward):
            self.currLocation+=1
        else:
            self.currLocation-=1
        self.log(f"Location is: {self.currLocation}")


    def turnLeft(self):
        self.motorL.set_power(-30)
        self.motorR.set_power(0)

    def turnRight(self):
        self.motorL.set_power(0)
        self.motorR.set_power(-30)

    def goForward(self):
        self.motorL.set_power(-25)
        self.motorR.set_power(-25)

    def stop(self):
        self.motorL.set_power(0)
        self.motorL.set_power(0)
    
    def goTowardsZone(self):
        """If it's going forward the delivery zone is to the right
        """
        self.log("go towards zone")
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
        self.log("go towards path")
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
        if not self.colorsToDeliver:
            self.log("all cubes have been delivered")
            self.rotateBackwards()
            return

        self.nextColor = self.colorsToDeliver.pop()
        self.log(f"next color: {self.nextColor}")
        curr = self.currLocation

        if curr == self.LAST_LOCATION:
            self.rotateBackwards()
        elif self.nextColor not in self.colorsInMap:
            self.rotateForward()
        else:
            next = self.colorsInMap.index(self.nextColor)
            if next > curr:
                self.rotateForward()
            else:
                self.rotateBackwards()

    def rotateForward(self):
        if not self.isForward:
            self.log("rotating forward")
            self.motorL.set_power(-30)
            self.motorR.set_power(30)
            sleep(self.TURN_180_TIME)
            self.motorL.set_power(0)
            self.motorR.set_power(0)
            self.isForward = True
    
    def rotateBackwards(self):
        if self.isForward:
            self.log("rotating backwards")
            self.motorL.set_power(-30)
            self.motorR.set_power(30)
            sleep(self.TURN_180_TIME)
            self.motorL.set_power(0)
            self.motorR.set_power(0)
            self.isForward = False

    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)

    def resetTimer(self):
        self.timer = time() + 1


if __name__ == '__main__':
    navigate = Navigation("A","B", 1, debug=True)
    try:
        navigate.navSequence()
    except BaseException:
        reset_brick()
        exit()