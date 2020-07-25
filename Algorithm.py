import math
import matplotlib.pyplot as plt

# Path loss exponent
PATH_LOSS = 5
# Environment constant
ENVIRONMENT_CONSTANT = 1
# Average RSSI value at d0
A0 = -50
# Device Constant for Normalization
DEVICE_CONSTANT = 0.5


# Modified Log Normal Shadowing Model
def getDistance(rssi):
    try:
        x = float((rssi - A0) / (-10 * PATH_LOSS))
        distance = (math.pow(10, x)) + ENVIRONMENT_CONSTANT
        return distance * DEVICE_CONSTANT
    except ZeroDivisionError:
        print("Path Loss cannot be Zero")


def createGraph():
    distanceVals = [getDistance(x) for x in range(-101, 0)]
    rssiVals = [x for x in range(-101, 0)]
    plt.plot(distanceVals, rssiVals, color="red", label="Disease Danger Zone")
    plt.plot(distanceVals[:30], rssiVals[:30], color="blue", label="Disease Safe Zone")
    plt.title("Modified Log Normal Shadowing Algorithm")
    plt.xlabel('Distance (Meters)')
    plt.ylabel('RSSI Values (dBm)')
    plt.legend()
    plt.savefig('AlgorithmGraphs/ModelGraph.png')


if __name__ == '__main__':
    createGraph()
