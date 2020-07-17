import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy.interpolate import make_interp_spline, BSpline


def getRSSI(file):
    # rows + RSSI Values
    rows = []
    RSSIVal = []
    # Parse CSV File
    with open(file, 'r') as f:
        # CSV Reader
        reader = csv.reader(f, delimiter=',')
        # Append
        for line in reader:
            rows.append(line)
        f.close()
    # Counter to skip first element in rows
    counter = 0
    # Parse Contents of CSV File
    for element in rows:
        if counter == 0:
            counter += 1
            continue
        # Get RSSI Values
        RSSIVal.append(element[-1])
    RSSIVal = [int(i) for i in RSSIVal]
    return RSSIVal


def getIteration(file):
    # Rows = Scan Number lists
    rows = []
    scanNum = []
    # Parse CSV File
    with open(file, 'r') as f:
        # CSV Reader
        reader = csv.reader(f, delimiter=',')
        # Append lines to rows
        for line in reader:
            rows.append(line)
            # Close CSV file
        f.close()
    # Counter to skip first element in rows
    counter = 0
    # Parse Contents of CSV File
    for element in rows:
        if counter == 0:
            counter += 1
            continue
        # Get RSSI Values
        scanNum.append(element[0])
    scanNum = [int(i) for i in scanNum]
    return scanNum


def getRSSIGraphs():
    for x in range(11):
        if x % 2 == 0:
            # RSSI Values for Boxes + No Boxes
            noBoxRSSI = getRSSI('NoBoxData/noBox' + str(x) + '.csv')
            boxRSSI = getRSSI('BoxData/box' + str(x) + '.csv')
            # Scan values for Boxes + No Boxes
            noBoxScans = getIteration('NoBoxData/noBox' + str(x) + '.csv')
            boxScans = getIteration('BoxData/box' + str(x) + '.csv')
            # Range Limit
            plt.ylim(min(noBoxRSSI) - 20, max(noBoxRSSI) + 20)
            # Get first 50 scans
            plt.xlim(0, 51)
            # X scale
            plt.xticks(np.arange(0, 51, 2.0))
            # Axes Labels
            plt.xlabel('Scan Number')
            plt.ylabel('RSSI Value (dBm)')
            # Title
            plt.title(str(x) + " Meters RSSI Values")
            # Smoothen Graph
            xNoBoxNew = np.linspace(min(noBoxScans), max(noBoxScans), 600)
            xBoxNew = np.linspace(min(boxScans), max(boxScans), 600)
            spl = make_interp_spline(noBoxScans, noBoxRSSI, k=3)
            spl2 = make_interp_spline(boxScans, boxRSSI, k=3)
            newNoBox = spl(xNoBoxNew)
            newBox = spl2(xBoxNew)

            # Plot Graph
            plt.plot(xNoBoxNew, newNoBox, "-b", label="No BoxData")
            plt.plot(xBoxNew, newBox, "-r", label="Boxed")
            # Legend
            plt.legend(loc="upper right")
            # Save + close plot
            plt.savefig('RSSIGraphs/' + str(x) + "Meters")
            plt.close()


def getStandardDeviation(file):
    # RSSI Values
    RSSIValues = getRSSI(file)
    # Get Standard Deviation
    standardDeviation = round(statistics.stdev(RSSIValues), 3)
    return standardDeviation


def getMean(file):
    # RSSI Values
    RSSIValues = getRSSI(file)
    # Get Mean
    mean = round(statistics.mean(RSSIValues), 3)
    return mean


def getMeanGraph():
    boxMean = []
    noBoxMean = []
    # Get means for each distance (Boxed)
    for x in range(0, 11):
        if x % 2 == 0:
            boxMean.append(getMean('BoxData/box' + str(x) + '.csv'))

    # Get Means for each distance (No box)
    for x in range(0, 11):
        if x % 2 == 0:
            noBoxMean.append(getMean('NoBoxData/noBox' + str(x) + '.csv'))
    # Get Array for distances
    distances = [i * 2 for i in range(len(boxMean))]
    # Smoothen Graph
    xNew = np.linspace(min(distances), max(distances), 600)
    spl = make_interp_spline(distances, boxMean, k=3)
    spl2 = make_interp_spline(distances, noBoxMean, k=3)
    newBox = spl(xNew)
    newNoBox = spl2(xNew)

    # Plot Smooth Graphs
    plt.plot(xNew, newBox, "-b", label='Boxed RPi')
    plt.plot(xNew, newNoBox, "-r", label='Unboxed RPi')
    # Identify New Device
    plt.plot(xNew[480:], newBox[480:], color="magenta", label="Found New Device")
    plt.plot(xNew[480:], newNoBox[480:], color="magenta")
    # Legend
    plt.legend(loc="upper right")
    # Labels
    plt.xlabel('Distance (Meters)')
    plt.ylabel('RSSI Value (dBm)')

    # Add Title
    plt.title("Mean RSSI Values")
    plt.savefig('StatisticalGraphs/MeanGraph.png')
    plt.close()


def getSDGraph():
    boxSD = []
    noBoxSD = []
    # Get SD for each distance (Boxed)
    for x in range(0, 11):
        if x % 2 == 0:
            boxSD.append(getStandardDeviation('BoxData/box' + str(x) + '.csv'))

    # Get SD for each distance (No box)
    for x in range(0, 11):
        if x % 2 == 0:
            noBoxSD.append(getStandardDeviation('NoBoxData/noBox' + str(x) + '.csv'))
    # Get Array for distances
    distances = [i * 2 for i in range(len(boxSD))]
    # Smoothen Graph
    xNew = np.linspace(min(distances), max(distances), 600)
    spl = make_interp_spline(distances, boxSD, k=3)
    spl2 = make_interp_spline(distances, noBoxSD, k=3)
    newBox = spl(xNew)
    newNoBox = spl2(xNew)

    # Plot Smooth Graphs
    plt.plot(xNew, newBox, "-b", label='Boxed RPi')
    plt.plot(xNew, newNoBox, "-r", label='Unboxed RPi')
    # Identify New Device
    plt.plot(xNew[480:], newBox[480:], color="magenta", label="Found New Device")
    plt.plot(xNew[480:], newNoBox[480:], color="magenta")
    # Legend
    plt.legend(loc="upper right")
    # Labels
    plt.xlabel('Distance (Meters)')
    plt.ylabel('Standard Deviation')

    # Add Title
    plt.title("Standard Deviation of RSSI Values")
    plt.savefig('StatisticalGraphs/StandardDeviation.png')
    plt.close()


if __name__ == '__main__':
    getMeanGraph()
