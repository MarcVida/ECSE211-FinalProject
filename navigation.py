from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep, time
from color_detection import ColorDetector 
from statistics import mode

class Navigation:
    """Class for the navigation subsystem"""

    FORWARD_180_TIME = 0.1
    TURN_180_TIME = 1.17
    TURN_180_SPEED = 35
    TURN_SPEED = 40 #45
    TURN_PIVOT = 0.1    # 0 = the static wheel is the pivot, 1 = the center is the pivot
    FORWARD_SPEED = 25 #25
    TURN_DET_TIME = 0
    TURN_DET_MIN_TIME = 0.4    # minimum time the robot should turn
    TURN_DET_SPEED = 20
    FORWARD_DET_TIME = 0.8
    BACKWARDS_DET_TIME = 0.3

    FORWARD_TRY_TIME = 0.3 #0.5
    FORWARD_TRY_SPEED = 24 #15
    TURN_TRY_TIME = 0.5 #0.8
    TURN_TRY_SPEED = 20 #20
    OFFSET_TRY_TIME = 0 #0.2

    ROTATE_CAL_AMPLITUDE = 1 # 0 = doesn't rotate (do not try), 1 = rotates until perpenticular to green line, >1 = rotates even more

    PAUSE_DEL_TIME = 0.5

    colorDetector: ColorDetector = None
    motorR: Motor = None
    motorL: Motor = None
    isForward = True
    LAST_LOCATION = 6
    colorsInMap = [None] * (LAST_LOCATION + 1)
    colorsToDeliver = ["PURPLE","BLUE","GREEN","YELLOW","ORANGE"]
    nextColor = "RED"
    currLocation = 0
    timer = 0
    isFirstIteration = True


    def __init__(self, motorPortL: int, motorPortR: int, colorDetectorPort: int, debug: bool=False) -> None:
        """Constructor for the Navigation class.

        Args:
            motorPortL (int): The port for the left motor.
            motorPortR (int): The port for the right motor.
            colorDetector (ColorDetector): The ColorDetector object.
        """
        self.motorR = Motor(motorPortL)
        self.motorL = Motor(motorPortR)
        self.colorDetector = ColorDetector(colorDetectorPort)
        self.debug=debug

    def navSequence(self):
        self.resetTimer()
        while(True):
            color=self.colorDetector.getNavSensorColor()

            if color=="RED":
                if True:
                    if(self.isForward):
                        self.turnLeft()
                    else:
                        self.turnRight()
                else:
                    if self.isForward:
                        self.rotate(-self.TURN_SPEED)
                    else:
                        self.rotate(self.TURN_SPEED)

            elif color=="BLUE":
                if True:
                    if(self.isForward):
                        self.turnRight()
                    else:
                        self.turnLeft()
                else:
                    if self.isForward:
                        self.rotate(self.TURN_SPEED)
                    else:
                        self.rotate(-self.TURN_SPEED)

            elif (color=="GREEN" or color=="YELLOW") and time() > self.timer:
                # Update location, return a flag if necessary
                # If DELIVERY flag is returned, the main module must call turnTowardsNextLocation() after the delivery
                self.stop()
                self.updateLocation()
                self.log(f"current location: index={self.currLocation}, color={self.colorsInMap[self.currLocation]}")
                #self.calibrateDirection()
                if self.isFirstIteration:
                    if self.currLocation <= 0:
                        self.rotateForward()
                        self.currLocation = 0
                        self.isFirstIteration = False
                    elif self.isForward:
                        self.goTowardsZone()
                        #zoneColor = self.colorDetector.getNavSensorColor()
                        zoneColor = self.tryToDetectColor2() # TODO: Try using tryToDetectColor2()
                        self.log(f"detected color: {zoneColor}")
                        if zoneColor in self.colorsInMap:
                            zoneColor = "DUMMY"
                        self.colorsInMap[self.currLocation] = zoneColor
                        self.log(f"colors in map update: {self.colorsInMap}")
                        self.goTowardsPath()
                        if zoneColor == self.nextColor:
                            sleep(self.PAUSE_DEL_TIME)
                            return "DELIVERY"
                        if self.currLocation >= self.LAST_LOCATION:
                            self.currLocation = self.LAST_LOCATION
                            self.rotateBackwards()
                else:
                    if self.currLocation <= 0:
                        self.rotateForward()
                        self.currLocation = 0
                        if not self.nextColor:
                            self.colorsToDeliver = ["PURPLE","BLUE","GREEN","YELLOW","ORANGE"]
                            self.nextColor = "RED"
                            return "LOADING"
                    elif self.isForward and self.colorsInMap[self.currLocation] == self.nextColor:
                        self.stop()
                        #self.calibrateDirection() # TODO: verify if it works
                        sleep(self.PAUSE_DEL_TIME)
                        return "DELIVERY"
                    elif self.isForward and (self.nextColor not in self.colorsInMap) and self.colorsInMap[self.currLocation] == "DUMMY":
                        self.stop()
                        self.colorsInMap[self.currLocation] = self.nextColor
                        self.log(f"colors in map update (dummy color replaced): {self.colorsInMap}")
                        #self.calibrateDirection() # TODO: verify if it works
                        sleep(self.PAUSE_DEL_TIME)
                        return "DELIVERY"
                    self.log("no delivery")
                    if self.currLocation >= self.LAST_LOCATION:
                        self.currLocation = self.LAST_LOCATION
                        self.rotateBackwards()
                self.resetTimer()
            
            else:
                self.goForward()

            sleep(0.01)

    """def navSequence(self):
        self.resetTimer()
        while(True):
            color=self.colordetector.getNavSensorColor()

            if color=="RED":
                if(self.isForward):
                    self.turnLeft()
                else:
                    self.turnRight()

            elif color=="BLUE":
                if(self.isForward):
                    self.turnRight()
                else:
                    self.turnLeft()

            elif (color=="GREEN" or color=="YELLOW") and time() > self.timer:
                # Update location, return DELIVERY flag if correct location
                # If DELIVERY flag is returned, the main module must call goTowardsPath() and turnTowardsNextLocation()
                self.stop()
                self.updateLocation()
                self.log(f"current location: index={self.currLocation}, color={self.colorsInMap[self.currLocation]}")
                if self.currLocation <= 0:
                    self.rotateForward()
                    self.colorsToDeliver = ["YELLOW","PURPLE","BLUE","GREEN", "YELLOW", "ORANGE"]
                    self.nextColor = "RED"
                    self.currLocation = 0
                    return "LOADING"
                elif not self.colorsInMap[self.currLocation]:
                    self.goTowardsZone()
                    zoneColor = self.colordetector.getNavSensorColor()
                    self.colorsInMap[self.currLocation] = zoneColor
                    self.log(f"detected color: {zoneColor}")
                    self.log(f"colors in map update: {self.colorsInMap}")
                    if zoneColor == self.nextColor:
                        return "DELIVERY"
                    self.goTowardsPath()
                elif self.colorsInMap[self.currLocation] == self.nextColor:
                    self.goTowardsZone()
                    return "DELIVERY"
                self.log("no delivery")
                if self.currLocation == self.LAST_LOCATION:
                    self.rotateBackwards()
                self.resetTimer()
            
            else:
                self.goForward()

            sleep(0.01)"""

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
        self.motorR.set_power(self.TURN_SPEED)
        self.motorL.set_power(-self.TURN_SPEED * self.TURN_PIVOT)

    def turnRight(self):
        self.motorR.set_power(-self.TURN_SPEED * self.TURN_PIVOT)
        self.motorL.set_power(self.TURN_SPEED)

    def goForward(self, speed=FORWARD_SPEED):
        self.motorR.set_power(speed)
        self.motorL.set_power(speed)
        
    def goBackwards(self , speed=FORWARD_SPEED):
        self.motorR.set_power(-speed)
        self.motorL.set_power(-speed)

    def rotate(self, speed=TURN_180_SPEED):
        self.motorR.set_power(-speed)
        self.motorL.set_power(speed)

    def stop(self):
        self.motorR.set_power(0)
        self.motorL.set_power(0)
    
    def goTowardsZone(self):
        """If it's going forward the delivery zone is to the right
        """
        tempTimer = time()
        color = "GREEN"
        self.rotate(self.TURN_DET_SPEED)
        while color == "GREEN":
            color = self.colorDetector.getNavSensorColor()
        self.TURN_DET_TIME = time() - tempTimer
        if self.TURN_DET_TIME < self.TURN_DET_MIN_TIME:
            sleep(self.TURN_DET_MIN_TIME - self.TURN_DET_TIME)
            self.TURN_DET_TIME = self.TURN_DET_MIN_TIME
        self.goForward()
        sleep(self.FORWARD_DET_TIME)
        self.stop()

    def goTowardsPath(self):
        """Turn back to the road
        """
        self.goBackwards()
        sleep(self.FORWARD_DET_TIME)
        self.stop()
        self.rotate(-self.TURN_DET_SPEED)
        sleep(self.TURN_DET_TIME)
        self.goBackwards()
        sleep(self.BACKWARDS_DET_TIME)
        self.stop()
    
    def tryToDetectColor(self):
        color = "WHITE"
        tryTime = time() + self.OFFSET_TRY_TIME + self.FORWARD_TRY_TIME

        # Go forward
        self.goForward(self.FORWARD_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        
        # Rotate in both directions
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        tryTime = time() + (2 * self.TURN_TRY_TIME)
        self.rotate(-self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()

        # Go backwards
        tryTime = time() + self.FORWARD_TRY_TIME
        self.goBackwards(self.FORWARD_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()

        # Rotate in both directions
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        tryTime = time() + (2 * self.TURN_TRY_TIME)
        self.rotate(-self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()

        # Go backwards
        tryTime = time() + self.OFFSET_TRY_TIME
        self.goBackwards(self.FORWARD_TRY_SPEED)
        while time() < tryTime:
            if color == "WHITE": color = self.colorDetector.getNavSensorColor()
        self.stop()
        
        return color
    
    def tryToDetectColor2(self):
        colors = []
        tryTime = time() + self.OFFSET_TRY_TIME + self.FORWARD_TRY_TIME

        # Go forward
        self.goForward(self.FORWARD_TRY_SPEED)
        #self.pollZoneColor(colors, tryTime)
        sleep(self.self.OFFSET_TRY_TIME + self.FORWARD_TRY_TIME)
        self.stop()
        
        # Rotate in both directions
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()
        tryTime = time() + (2 * self.TURN_TRY_TIME)
        self.rotate(-self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()

        # Go backwards
        tryTime = time() + self.FORWARD_TRY_TIME
        self.goBackwards(self.FORWARD_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()

        # Rotate in both directions
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()
        tryTime = time() + (2 * self.TURN_TRY_TIME)
        self.rotate(-self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()
        tryTime = time() + self.TURN_TRY_TIME
        self.rotate(self.TURN_TRY_SPEED)
        self.appendZoneColor(colors, tryTime)
        self.stop()

        # Go backwards
        tryTime = time() + self.OFFSET_TRY_TIME
        self.goBackwards(self.FORWARD_TRY_SPEED)
        sleep(self.OFFSET_TRY_TIME)
        self.stop()
        
        return mode(colors) if colors else "DUMMY"
    
    def appendZoneColor(self, colors: list, tryTime):
        """Continuously appends detected colors for some time"""
        while time() < tryTime:
            color = self.colorDetector.getNavSensorColor()
            if color != "WHITE": colors.append(color)
        
    def calibrateDirection(self):
        # Rotate to the left until green line is not detected
        color = "GREEN"
        prevColor = "GREEN"
        self.rotate(-self.TURN_TRY_SPEED)
        while "GREEN" in [prevColor, color]:
            prevColor = color
            color = self.colorDetector.getNavSensorColor()

        # Rotate to the right until green line is not detected
        tempTimerR = time()
        color = "GREEN"
        prevColor = "GREEN"
        self.rotate(self.TURN_TRY_SPEED)
        sleep(0.3)
        while "GREEN" in [prevColor, color]:
            prevColor = color
            color = self.colorDetector.getNavSensorColor()
        tempTimerR = time() - tempTimerR

        # Rotate to the left until robot is perpenticular to the green line
        rotateBackTime = tempTimerR / 2
        self.rotate(-self.TURN_TRY_SPEED)
        sleep(rotateBackTime * self.ROTATE_CAL_AMPLITUDE)
        self.stop()
            
    def turnTowardsNextLocation(self):
        if not self.colorsToDeliver:
            self.log("all cubes have been delivered")
            self.nextColor = None
        else:
            self.nextColor = self.colorsToDeliver.pop()
            self.log(f"next color: {self.nextColor}")
            if self.currLocation >= self.LAST_LOCATION:
                self.currLocation = self.LAST_LOCATION
                self.rotateBackwards()
            else:
                self.goBackwards()
                sleep(self.BACKWARDS_DET_TIME * 0.8)
                self.stop()

        """if not self.colorsToDeliver:
            self.log("all cubes have been delivered")
            self.rotateBackwards()
            return

        self.nextColor = self.colorsToDeliver.pop()
        self.log(f"next color: {self.nextColor}")"""
        """curr = self.currLocation

        if curr == self.LAST_LOCATION:
            self.rotateBackwards()
        elif self.nextColor not in self.colorsInMap:
            self.rotateForward()
        else:
            next = self.colorsInMap.index(self.nextColor)
            if next > curr:
                self.rotateForward()
            else:
                self.rotateBackwards()"""

    def rotateForward(self):
        if not self.isForward:
            self.log("rotating forward")
            self.goForward()
            sleep(self.FORWARD_180_TIME)
            self.motorR.set_power(-self.TURN_180_SPEED)
            self.motorL.set_power(self.TURN_180_SPEED)
            sleep(self.TURN_180_TIME)
            self.stop()
            self.isForward = True
    
    def rotateBackwards(self):
        if self.isForward:
            self.log("rotating backwards")
            self.goForward()
            sleep(self.FORWARD_180_TIME)
            self.rotate(self.TURN_180_SPEED)
            sleep(self.TURN_180_TIME)
            self.stop()
            self.isForward = False

    def log(self, message: str):
        """Prints a message is debug is set to True.

        Args:
            message (str): The message to be printed
        """
        if self.debug: print(message)

    def resetTimer(self):
        self.timer = time() + 1.3


if __name__ == '__main__':
    navigate = Navigation("A","B", 1, debug=True)
    try:
        navigate.navSequence()
    except BaseException:
        reset_brick()
        exit()