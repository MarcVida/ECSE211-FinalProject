from navigation import Navigation
from color_detection import ColorDetector
from delivery import Delivery

def waitUntil(callback):
    while not callback():
        pass

if __name__ == "__main__":
    nav = Navigation()
    deliv = Delivery()

    """
    FIRST ITERATION:
    1 - cube loading (wait until button pressed)
    2 - navigation sequence
    3 - when stop reached, check case:
        a - green stop:
            1. save color & position to system
            2. if correct color, drop cube
        b - yellow stop: go to step 1
    4 - go to step 2

    NEXT ITERATIONS:
    1 - cube loading (wait until button pressed)
    2 - navigation sequence
    3 - when stop reached, check case:
        a - green stop: 
            1. track new position
            2. if correct position:
                a. drop cube
                b. set direction towards next position (?)
        b - yellow stop: go to step 1
    4 - go to step 2
    """