from utils.brick import EV3ColorSensor, wait_ready_sensors, Motor
from time import sleep
import color_detection 

""" Class for robot to navigate the map"""
class Navigation:
    colordetector:color_detection.ColorDetector=None
    motorL: Motor=None
    motorR:Motor = None

    def __init__(self, motorPortL, motorPortR, colorDetector)->None:
        self.motorL=Motor(motorPortL)
        self.motorR=Motor(motorPortR)
        self.colordetector=colorDetector


    def navSequence(self):
        navSensor=EV3ColorSensor(None)

        while(True):
            color=self.colordetector.getNavSensorColor()

            if color=="BLUE":
                self.motorL.set_power(30)
                self.motorR.set_power(0)
                sleep(0.1)

            elif color=="RED":
                self.motorL.set_power(0)
                self.motorR.set_power(30)
                sleep(0.1)
                pass
            
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


if __name__=='__main__':
    navSequence()
    #instantiate flute
