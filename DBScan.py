import sklearn
from sklearn import datasets
import pandas as pd
import numpy
from scipy.spatial import distance
from numpy.random import permutation


# Creating dataset
points, membershipArray = datasets.make_moons(
    n_samples=200, shuffle=True, noise=None, random_state=None)


# Saving dataset as CSV (Not saving 2nd array as we will determine membership on our own)
pd.DataFrame(points).to_csv(
    "C:\\Users\\Haider Zia\\Desktop\\Data Mining\\A1-DB Scan-DM\\points.csv")


# Reading back from saved CSV
df = pd.read_csv(
    "C:\\Users\\Haider Zia\\Desktop\\Data Mining\\A1-DB Scan-DM\\points.csv")
pointsCSV = df.values.tolist()
print(pointsCSV)

# Creating new list with added attribute for category
array_length = len(pointsCSV)
categorizedPoints = []
for i in range(array_length):
    elements = (pointsCSV[i][1], pointsCSV[i][2], 'Uncategorized')
    categorizedPoints.append(elements)


# DB Scan
epsilon = 0.3
minPoints = 10
for i in permutation(array_length):  # Randomly pick points from data
    pointsInRadius = 0
    queue = []
    for j in range(array_length):  # Check epsilon radius around the picked data point
        if(i != j):
            pointA = (pointsCSV[i][1], pointsCSV[i][2])
            pointB = (pointsCSV[j][1], pointsCSV[j][2])
            if(distance.euclidean(pointA, pointB) < epsilon):
                pointsInRadius = pointsInRadius+1
                if(categorizedPoints[j][2] == 'Uncategorized' or categorizedPoints[j][2] == 'Outlier'):
                    # Add non-core points to queue, this queue will only be used if this point is itself a core point
                    queue.append(j)

    if (pointsInRadius > minPoints):
        print("Core")
        categorizedPoints[i] = (categorizedPoints[i][0],
                                categorizedPoints[i][1], 'Core')
        queueLength = len(queue)
        # Iterate through queue of points around this core point
        while queue:
            pointsInRadius2 = 0
            currentQueuePoint = queue.pop(0)
            for k in range(array_length):
                if(currentQueuePoint != k):
                    pointA = (pointsCSV[currentQueuePoint]
                              [1], pointsCSV[currentQueuePoint][2])
                    pointB = (pointsCSV[k][1], pointsCSV[k][2])
                    if(distance.euclidean(pointA, pointB) < epsilon):
                        if(categorizedPoints[k][2] == 'Uncategorized' or categorizedPoints[k][2] == 'Outlier'):
                            pointsInRadius2 = pointsInRadius2+1
            if(pointsInRadius2 > minPoints):
                categorizedPoints[currentQueuePoint] = (
                    categorizedPoints[currentQueuePoint][0], categorizedPoints[currentQueuePoint][1], 'Core')
                print("Core")
            else:
                categorizedPoints[currentQueuePoint] = (
                    categorizedPoints[currentQueuePoint][0], categorizedPoints[currentQueuePoint][1], 'Border')
                print("Border")
    else:
        print("Outlier")
        categorizedPoints[i] = (categorizedPoints[i][0],
                                categorizedPoints[i][1], 'Outlier')


print(categorizedPoints)
pd.DataFrame(categorizedPoints).to_csv(
    "C:\\Users\\Haider Zia\\Desktop\\Data Mining\\A1-DB Scan-DM\\categorizedPoints.csv")
