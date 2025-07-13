import pandas as pd
import random
from datetime import datetime, timedelta

devices = ['D-1', 'D-2', 'D-3']
locations = ['Pune', 'Mumbai', 'Banglore']
startDate = datetime(2024, 1, 1)
data = []

for i in range(720):  
    date = startDate + timedelta(days=i)
    for device in devices:
        location = random.choice(locations)
        plannedTime = 480                  
        runTime = random.randint(300, 480)
        idealCycleTime = round(random.uniform(0.4, 0.6), 2)
        totalUnits = int(runTime / idealCycleTime)
        goodUnits = int(totalUnits * random.uniform(0.9, 1.0))  
        data.append([
            device, location, date.strftime("%Y-%m-%d"), plannedTime,
            runTime, idealCycleTime, totalUnits, goodUnits
        ])

df = pd.DataFrame(data, columns=[
    'Device ID', 'Location', 'Date', 'Planned Time',
    'Run Time', 'Ideal Cycle Time', 'Total Units', 'Good Units'
])

df.to_excel("sensor_data.xlsx", index=False)
