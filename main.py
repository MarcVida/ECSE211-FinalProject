from navigation import Navigation
from color_detection import ColorDetector
from delivery import Delivery
from utils.brick import reset_brick

if __name__ == "__main__":
    navigate = Navigation("B","C", 1, debug=True)
    #delivery = Delivery("D", 999, debug=True)
    try:
        while True:
            flag = navigate.navSequence()
            if flag == "DELIVERY":
                # TODO: do delivery
                #delivery.deliverySequence()
                print("DELIVERY")
                navigate.goTowardsPath()
                #navigate.turnTowardsNextLocation()
            elif flag == "LOADING":
                # TODO: do loading
                #delivery.loadingSequence()
                print("LOADING")
                pass
    except BaseException as e:
        reset_brick()
        raise e
        #exit()

    """while(True):
        deliv.loadingSequence()
        deliv.isLoadingComplete()
        
        while(True):
           instruction=nav.navSequence()
           if(instruction=="Delivery"):
               deliv.deliverySequence()
           else:
               break"""
            

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