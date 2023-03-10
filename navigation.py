from utils.brick import EV3ColorSensor
from math import sqrt

class colorDetector:

    COLORS = {}
    COLOR_TRESHOLD = 1

    def __init__(self, navigationPort, deliveryPort) -> None:
        self.navSensor = EV3ColorSensor(navigationPort)
        self.delSensor = EV3ColorSensor(deliveryPort)
    
    def get_color_name(self, rgb: list):
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
        distances = {color: 0 for color in self.COLORS.keys()}
        for color in self.COLORS.items():
            difference = [color[1][0] - normRBG[0], color[1][0] - normRBG[1], color[1][2] - normRBG[2]]
            distances[color[0]] = (sqrt(difference[0]**2 + difference[1]**2 + difference[2]**2))
        minDistance = min(distances.values())

        # return detected color
        if minDistance > self.colorTreshold:
            return "Unknown"
        for color in distances.items():
            if color[1] == minDistance:
                return color[0]
