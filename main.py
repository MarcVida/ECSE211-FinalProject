from navigation import Navigation
from delivery import Delivery
from utils.brick import reset_brick, wait_ready_sensors

if __name__ == "__main__":
    # Instantiate components
    navigate = Navigation("B","C", 1, debug=True)
    delivery = Delivery("D", 2, debug=True)
    wait_ready_sensors()

    try:
        # Start the program loop
        delivery.loadingSequence()
        while True:
            flag = navigate.navSequence()
            if flag == "DELIVERY":
                print("DELIVERY")
                delivery.deliverySequence()
                navigate.turnTowardsNextLocation()
            elif flag == "LOADING":
                delivery.loadingSequence()
    except BaseException as e:
        # Terminate the program
        reset_brick()
        exit()