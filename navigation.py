from utils.brick import EV3ColorSensor, wait_ready_sensors
from math import sqrt

class ColorDetector:
    """Class for the color detection algorithm.
    """

    #TODO: Set color value for each color
    COLORS = {
        "SAMPLE_NAME": [0,0,0]
    }
    COLOR_TRESHOLD = 1

    navSensor: EV3ColorSensor = None
    delSensor: EV3ColorSensor = None

    def __init__(self, navigationPort, deliveryPort) -> None:
        """Constructor for the color_detector class.

        Args:
            navigationPort (_type_): _description_
            deliveryPort (_type_): _description_
        """
        if (not self.navSensor): self.navSensor = EV3ColorSensor(navigationPort)
        if (not self.delSensor): self.delSensor = EV3ColorSensor(deliveryPort)
        wait_ready_sensors()
    
    def getColorName(self, rgb: list):
        # normalize the values to be between 0 and 1

        ### UNIT-VECTOR METHOD ###
        # denominator = sqrt(r ** 2 + g ** 2 + b ** 2)

        ### RATIO METHOD ###
        denominator = sum(rgb)
        
        red = (rgb[0] / denominator)
        green = (rgb[1] / denominator)
        blue = (rgb[2] / denominator)
        normRBG = [red, green, blue]

        # compare normalized rbg to reference values
        distances = {}
        for colorName, colorRGB in self.COLORS.items():
            difference = [colorRGB[0] - normRBG[0], 
                          colorRGB[0] - normRBG[1], 
                          colorRGB[2] - normRBG[2]]
            distance = sqrt(difference[0]**2 + difference[1]**2 + difference[2]**2)
            if distance <= self.COLOR_TRESHOLD:
                distances[colorName] = distance

        # return detected color
        if not distances:
            return "Unknown"
        minDistance = min(distances.values())
        for colorName, distance in distances.items():
            if distance == minDistance:
                return colorName
