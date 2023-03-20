from navigation import Navigation
from color_detection import ColorDetector
from delivery import Delivery

if __name__ == "__main__":
    nav = Navigation("A","B")
    deliv = Delivery()

    while(True):
        deliv.loadingSequence()
        deliv.isLoadingComplete()
        
        while(True):
           instruction=nav.navSequence()
           if(instruction=="Delivery"):
               deliv.deliverySequence()
           else:
               break
            

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