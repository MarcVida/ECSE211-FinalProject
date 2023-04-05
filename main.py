from navigation import Navigation
from color_detection import ColorDetector
from delivery import Delivery
from utils.brick import reset_brick
from time import sleep

if __name__ == "__main__":
    navigate = Navigation("B","C", 1, debug=True)
    delivery = Delivery("D", 2, debug=True)
    try:
        delivery.loadingSequence()
        while True:
            flag = navigate.navSequence()
            if flag == "DELIVERY":
                print("DELIVERY")
                delivery.deliverySequence()
                navigate.turnTowardsNextLocation()
            elif flag == "DELIVERY BACK":
                print("DELIVERY BACK")
                delivery.deliverySequence()
                navigate.goForward()
                sleep(1.4)
                navigate.turnTowardsNextLocation()
            elif flag == "LOADING":
                delivery.loadingSequence()
    except BaseException as e:
        reset_brick()
        raise e
        #exit()            

    """
    FIRST ITERATION:
    1 - cube loading (wait until button pressed)
    2 - navigation sequence
    3 - when stop reached, check case:
        a - green stop:
            1. save delivery zone color & position to system
            2. if correct color, drop cube
            3. go to step 2
        b - yellow stop: rotate 180 degrees, then go to step 1

    NEXT ITERATIONS:
    1 - cube loading (wait until button pressed)
    2 - navigation sequence
    3 - when stop reached, check case:
        a - green stop: 
            1. track new position
            2. if correct position:
                a. drop cube
                b. set direction towards next position
            3. go to step 2
        b - yellow stop: rotate 180 degrees, then go to step 1
    """