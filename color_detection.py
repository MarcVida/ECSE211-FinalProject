from utils.brick import EV3ColorSensor, wait_ready_sensors
from math import sqrt
from statistics import mode
from time import sleep

class ColorDetector:
    """Class for the color detection algorithm."""

    ################# CONSTANTS #################

    COLORS = {
        "BLUE": [0.2309846, 0.4239539, 0.3450615],
        "GREEN": [0.1969103, 0.6920012, 0.1110885],
        "ORANGE": [0.7610474,0.1759241,0.0630284],
        "PURPLE": [0.7344298, 0.1123536, 0.1532166],
        "RED": [0.8353416,0.0939238,0.0707346],
        "WHITE": [0.3760506, 0.4383683, 0.1855811],
        "YELLOW": [0.4501223, 0.5066404, 0.0432373],
    }
    COLOR_TRESHOLD = 0.3

    ################# VARIABLES #################

    navSensor: EV3ColorSensor = None

    ################## METHODS ##################

    def __init__(self, navigationPort: int) -> None:
        """Constructor for the ColorDetector class.

        Args:
            navigationPort (int): The port of the navigation color sensor
            deliveryPort (int): The port of the delivery color sensor
        """
        if (not self.navSensor): self.navSensor = EV3ColorSensor(navigationPort)
        wait_ready_sensors()
    
    def getColorName(self, rgb: list) -> str:
        """Gets the color name from the given RGB values.
        Returns "UNKNOWN" if no color is detected. Returns None if rgb is empty.

        Args:
            rgb (list): the RGB values of the color to be detected

        Returns:
            str: The name of the detected color.
        """
        if not any(rgb): return None

        # normalize the values to be between 0 and 1

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
                          colorRGB[1] - normRBG[1], 
                          colorRGB[2] - normRBG[2]]
            distance = sqrt((difference[0]**2) + (difference[1]**2) + (difference[2]**2))
            if distance <= self.COLOR_TRESHOLD:
                distances[colorName] = distance

        # return detected color
        if not distances:
            return "UNKNOWN"
        minDistance = min(distances.values())
        for colorName, distance in distances.items():
            if distance == minDistance:
                return colorName
            
    def getNavSensorColor(self) -> str:
        """Returns the name of the color detected by the navigation sensor."""
        colors = []
        for _ in range(5):
            colors.append(self.getColorName(self.navSensor.get_rgb()))
            sleep(0.005)
        return mode(colors)
