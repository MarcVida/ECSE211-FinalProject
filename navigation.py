from utils.brick import Motor, reset_brick
from time import sleep, time
from color_detection import ColorDetector 
from statistics import mode

class Navigation:
    """Class for the navigation subsystem"""

    ################# CONSTANTS #################

    LAST_LOCATION = 6           # Sets the index of the last location of a map

    FORWARD_180_TIME = 0.1      # Sets how long to go forward before turning backwards 180 degrees
    TURN_180_TIME = 1.1         # Sets how long to rotate during a 180 degree turn
    TURN_180_SPEED = 35         # Sets the rotation speed during a 180 degree turn
    TURN_SPEED = 32             # Sets the turning speed during a turn
    TURN_PIVOT = 0              # 0 = the static wheel is the pivot, 1 = the center is the pivot
    FORWARD_SPEED = 25          # Sets the forward speed
    TURN_DET_MIN_TIME = 0.6     # Sets how long to turn at least when turning towards the zone/path
    TURN_DET_SPEED = 20         # Sets the rotation speed when turning towards the zone/path
    FORWARD_DET_TIME = 0.8      # Sets how long to go forward after/before turning towards the zone/path
    BACKWARDS_DET_TIME = 0.15   # Sets how long to go backwards after turning towards the path

    FORWARD_TRY_TIME = 0.3      # Sets how long to go forward during the color detection sequence
    FORWARD_TRY_SPEED = 20      # Sets the forward speed during the color detection sequence
    TURN_TRY_TIME = 0.4         # Sets how long to rotate during the color detection sequence
    TURN_TRY_SPEED = 20         # Sets the rotation speed during the color detection sequence 
    OFFSET_TRY_TIME = 0.0       # Sets how long to go forward before & after the color detection sequece

    PAUSE_DEL_TIME = 0.5        # Sets the pause time before returning the DELIVERY flag

    ################# VARIABLES #################

    colorDetector: ColorDetector = None
    motorR: Motor = None
    motorL: Motor = None
    isForward = True
    colorsInMap = [None] * (LAST_LOCATION + 1)
    colorsToDeliver = ["PURPLE","BLUE","GREEN","YELLOW","ORANGE"]
    nextColor = "RED"
    currLocation = 0
    turnDetTime = 0
    timer = 0
    fwdTimer = 0
    turnBackTimer = 0
    isFirstIteration = True
    needsToTurnBack = False

    ################## METHODS ##################

    def __init__(self, motorPortL: int, motorPortR: int, colorDetectorPort: int, debug: bool = False) -> None:
        """Constructor for the Navigation class.

        Args:
            motorPortL (int): The port for the left motor.
            motorPortR (int): The port for the right motor.
            colorDetector (ColorDetector): The ColorDetector object.
        """
        self.motorR = Motor(motorPortL)
        self.motorL = Motor(motorPortR)
        self.colorDetector = ColorDetector(colorDetectorPort)
        self.debug = debug

    def navSequence(self):
        """Navigation sequence. Returns 'YELLOW' or 'DELIVERY'."""
        self.resetTimer()
        while(True):
            if time() < self.fwdTimer:
                self.goForward()
                sleep(self.fwdTimer - time())
                continue
            
            color = self.colorDetector.getNavSensorColor()
            
            if self.needsToTurnBack and time() > self.turnBackTimer:
                self.needsToTurnBack = False
                self.rotateForward()

            if color=="RED" and time() > self.fwdTimer:
                if(self.isForward):
                    self.turnLeft()
                else:
                    self.turnRight()

            elif (color=="WHITE" or color=="BLUE") and time() > self.fwdTimer:
                if(self.isForward):
                    self.turnRight()
                else:
                    self.turnLeft()

            elif (color=="GREEN" or color=="YELLOW") and time() > self.timer:
                # Update location, return a flag if necessary
                # If DELIVERY flag is returned, the main module must call turnTowardsNextLocation() after the delivery
                self.stop()
                sleep(0.15)
                
                self.updateLocation()
                self.log(f"current location: index={self.currLocation}, color={self.colorsInMap[self.currLocation]}")
                
                if self.isFirstIteration:
                    if self.currLocation <= 0:
                        self.rotateForward()
                        self.currLocation = 0
                        self.isFirstIteration = False
                    elif self.isForward:
                        self.goTowardsZone()
                        zoneColor = self.tryToDetectColor()
                        self.log(f"detected color: {zoneColor}")
                        if zoneColor in self.colorsInMap:
                            zoneColor = "DUMMY"
                        self.colorsInMap[self.currLocation] = zoneColor
                        self.log(f"colors in map update: {self.colorsInMap}")
                        self.goTowardsPath()
                        if self.currLocation >= self.LAST_LOCATION:
                            self.currLocation = self.LAST_LOCATION
                            self.isFirstIteration = False
                            self.rotateBackwards()
                else:
                    if self.currLocation <= 0:
                        self.rotateForward()
                        self.currLocation = 0
                        if not self.nextColor:
                            self.colorsToDeliver = ["PURPLE","BLUE","GREEN","YELLOW","ORANGE"]
                            self.nextColor = "RED"
                            return "LOADING"
                    elif self.colorsInMap[self.currLocation] == self.nextColor:
                        if self.isForward:
                            self.stop()
                            sleep(self.PAUSE_DEL_TIME)
                            return "DELIVERY"
                        else:
                            self.needsToTurnBack = True
                            self.resetTurnBackTimer()
                            self.currLocation -= 1
                        
                    elif self.isForward and (self.nextColor not in self.colorsInMap) and self.colorsInMap[self.currLocation] == "DUMMY":
                        self.goForward()
                        sleep(0.2)
                        self.stop()
                        self.colorsInMap[self.currLocation] = self.nextColor
                        self.log(f"colors in map update (dummy color replaced): {self.colorsInMap}")
                        sleep(self.PAUSE_DEL_TIME)
                        return "DELIVERY"
                    self.log("no delivery")
                    if self.currLocation >= self.LAST_LOCATION:
                        self.currLocation = self.LAST_LOCATION
                        self.rotateBackwards()
                self.resetTimer()
                
            else:
                self.goForward()

    def updateLocation(self):
        """Keep track of position relative to the yellow/green lines on the map
        There are 7 total yellow/green lines."""
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
        tempTimer = time()
        color = "GREEN"
        self.rotate(self.TURN_DET_SPEED)
        while color == "GREEN":
            color = self.colorDetector.getNavSensorColor()
        self.turnDetTime = time() - tempTimer
        if self.turnDetTime < self.TURN_DET_MIN_TIME:
            sleep(self.TURN_DET_MIN_TIME - self.turnDetTime)
            self.turnDetTime = self.TURN_DET_MIN_TIME
        self.goForward()
        sleep(self.FORWARD_DET_TIME)
        self.stop()

    def goTowardsPath(self):
        self.goBackwards()
        sleep(self.FORWARD_DET_TIME)
        self.stop()
        self.rotate(-self.TURN_DET_SPEED)
        sleep(self.turnDetTime)
        self.goBackwards()
        sleep(self.BACKWARDS_DET_TIME)
        self.stop()
    
    def tryToDetectColor(self):
        """Delivery zone color detection sequence."""
        colors = []
        tryTime = time() + self.OFFSET_TRY_TIME + self.FORWARD_TRY_TIME

        # Go forward
        self.goForward(self.FORWARD_TRY_SPEED)
        sleep(self.OFFSET_TRY_TIME + self.FORWARD_TRY_TIME)
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
    
    def appendZoneColor(self, colors: list, tryTime: float):
        """Continuously appends detected colors for a finite duration.

        Args:
            colors (list): the color list to append to
            tryTime (float): the duration
        """
        while time() < tryTime:
            color = self.colorDetector.getNavSensorColor()
            if color != "WHITE": colors.append(color)
            
    def turnTowardsNextLocation(self):
        if not self.colorsToDeliver:
            self.log("all cubes have been delivered")
            self.nextColor = None
            self.rotateBackwards()
        else:
            self.nextColor = self.colorsToDeliver.pop()
            self.log(f"next color: {self.nextColor}")
            if self.currLocation >= self.LAST_LOCATION:
                self.currLocation = self.LAST_LOCATION
                self.rotateBackwards()
            elif not self.isFirstIteration:
                if self.nextColor in self.colorsInMap:
                    next=self.colorsInMap.index(self.nextColor)
                    if next > self.currLocation:
                        self.rotateForward()
                        
                    else:
                        self.rotateBackwards()
            self.stop()

    def rotateForward(self):
        """180 degree forward turn"""
        if not self.isForward:
            self.log("rotating forward")
            self.rotate(-self.TURN_180_SPEED)
            sleep(self.TURN_180_TIME)
            self.stop()
            self.isForward = True
    
    def rotateBackwards(self):
        """180 degree backwards turn"""
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
        self.timer = time() + 1.2
        self.resetFwdTimer()
        
    def resetFwdTimer(self):
        self.fwdTimer = time() + 0.3
        
    def resetTurnBackTimer(self):
        self.turnBackTimer = time() + 2.5


if __name__ == '__main__':
    """Test program"""
    navigate = Navigation("B","C", 1, debug=True)
    try:
        navigate.navSequence()
    except BaseException:
        reset_brick()
        exit()