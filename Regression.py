import numpy as np
from Graphs import getMean
import matplotlib.pyplot as plt


def createModel(xData, yData):
    model = np.poly1d(np.polyfit(xData, yData, 3))
    return model


def meanModelBoxed():
    # Get means for each distance (Boxed)
    boxMean = []
    for x in range(0, 11):
        if x % 2 == 0:
            boxMean.append(getMean('BoxData/box' + str(x) + '.csv'))

    distances = [i * 2 for i in range(len(boxMean))]
    return createModel(distances, boxMean)


def meanModelNoBox():
    noBoxMean = []

    # Get Means for each distance (No box)
    for x in range(0, 11):
        if x % 2 == 0:
            noBoxMean.append(getMean('NoBoxData/noBox' + str(x) + '.csv'))

    distances = [i * 2 for i in range(len(noBoxMean))]
    return createModel(distances, noBoxMean)


def graphModel(model, model2, path, yLim, xLim, xLabel, yLabel, title):
    x = np.arange(xLim)
    y = model(x)
    plt.plot(x, y, "-b", label="Boxed RPi")
    plt.ylim(yLim[0], yLim[1])

    x = np.arange(xLim)
    y = model2(x)
    plt.plot(x, y, "-r", label="No BoxData RPi")
    plt.ylim(yLim[0], yLim[1])

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    plt.title(title)
    plt.savefig(path)
    plt.close()


if __name__ == '__main__':
    model = meanModelBoxed()
    model2 = meanModelNoBox()
    graphModel(model, model2, 'RegressionGraphs/MeanRegression.png', [-100, -10], 11, 'Distance (Meters)', 'RSSI Value (dBm)',
               'Mean RSSI Regression')
