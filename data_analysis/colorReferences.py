"""This module computes the mean & stev of the rgb values for each csv file and stores them in
    ColorReferencesReport.txt while generating plots to visualize the results. This module uses
    part of the starter code from lab 2.
"""

from ast import literal_eval
from math import sqrt, e, pi
from statistics import mean, stdev

from matplotlib import pyplot as plt
import numpy as np

COLOR_SENSOR_DATA_FILES = ["blue.csv","green.csv","orange.csv","purple.csv","red.csv","white.csv","yellow.csv"]
NBR_DECIMAL_DIGITS = 7

color_report = ""

def gaussian(x, values):
    "Return a gaussian function from the given values."
    sigma = stdev(values)
    return (1 / (sigma * sqrt(2 * pi))) * e ** (-((x - mean(values)) ** 2) / (2 * sigma ** 2))

for fileName in COLOR_SENSOR_DATA_FILES:
    red, green, blue = [], [], []
    with open(fileName, "r") as f:
        for line in f.readlines():
            r, g, b = literal_eval(line)  # convert string to 3 floats
            # normalize the values to be between 0 and 1

            ### UNIT-VECTOR METHOD ###
            # denominator = sqrt(r ** 2 + g ** 2 + b ** 2)

            ### RATIO METHOD ###
            denominator = r + g + b
            
            red.append(r / denominator)
            green.append(g / denominator)
            blue.append(b / denominator)

    color_report += f"File:\t{fileName}\n"
    color_report += "Mean:\t"
    color_report += f"[{round(mean(red),NBR_DECIMAL_DIGITS)}"
    color_report += f",{round(mean(green),NBR_DECIMAL_DIGITS)}"
    color_report += f",{round(mean(blue),NBR_DECIMAL_DIGITS)}]\n"
    color_report += "Stdev:\t"
    color_report += f"r = {round(stdev(red),NBR_DECIMAL_DIGITS)}\t"
    color_report += f"g = {round(stdev(green),NBR_DECIMAL_DIGITS)}\t"
    color_report += f"b = {round(stdev(blue),NBR_DECIMAL_DIGITS)}\n\n"

    x_values = np.linspace(0, 1, 255)  # 255 evenly spaced values between 0 and 1
    plt.figure(fileName, figsize=(8,5))
    plt.plot(x_values, gaussian(x_values, red), color="r")
    plt.plot(x_values, gaussian(x_values, green), color="g")
    plt.plot(x_values, gaussian(x_values, blue), color="b")
    plt.xlabel("Normalized intensity value")
    plt.ylabel("Normalized intensity PDF by color")

with open("colorReferencesReport.txt", "w") as f:
    f.write(color_report)

plt.show()