import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    #Getting File paths
    files = ["Driver1EnduranceData.csv", "Driver2EnduranceData.csv"]
    # driverOnelapsCSVPath = []
    # for i in range(1,16):
    #     driverOnelapsCSVPath.append(f"Driver1 Lap {i}")
    # driverTwolapsCSVPath = []
    # for i in range(1,15):
    #     driverTwolapsCSVPath.append(f"Driver2 Lap {i}")
    # #Reading CSVs
    # for csvPath1, csvPath2 in zip(driverOnelapsCSVPath, driverTwolapsCSVPath):
    #     df =
    # Reading CSV
    driverOneDf = pd.read_csv(files[0])
    driverTwoDf = pd.read_csv(files[1])
    lapTimes = {
        'driverOneCumulativeTime': [113.901, 190.353, 261.857, 331.104, 398.652,
                                466.026, 536.357, 605.743, 671.024, 736.401,
                                808.066, 873.338, 938.436, 1003.34, 1083.0],

        'driverTwoCumulativeTime': [40.594, 117.581, 191.908, 264.67, 338.821,
                                413.768, 487.82, 561.371, 636.068, 708.539,
                                783.379, 862.935, 940.344, 1036.0],

        "driverOne": [113.901, 76.452, 71.504, 69.247, 67.548, 67.374, 70.331,
                    69.386, 65.281, 65.377, 71.665, 65.272, 65.098, 64.904, 79.66],
        "driverTwo": [40.594, 76.987, 74.327, 72.762, 74.151, 74.947, 74.052,
                    73.551, 74.697, 72.471, 74.84, 79.556, 77.409, 95.656],
    }




    # for header in driverOne.columns:
    #     ax = driverOne.plot.scatter(x="Time (s)", y=header, color="DarkBlue")
    #     driverTwo.plot.scatter(x="Time (s)", y=header, color="DarkRed", ax = ax)
    #     plt.show()
    # print(driverOne['Time (s)'].tail(5))
    # print(driverTwo['Time (s)'].tail(5))

######
# To DO
# Compate length of times since not same
