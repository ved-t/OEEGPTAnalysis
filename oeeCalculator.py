import pandas as pd
from oeeModels import OEE
from colorama import Fore, Style, init

# OEE calculator
def calculateOEE(df, oeeData: OEE) -> str:
    try:
        # extract the required paramaetrs from user's query
        devideId = oeeData.deviceId
        location = oeeData.location
        year = oeeData.year
        month = oeeData.month
        day = oeeData.day

        # Get the specific device
        mask = (
            (df['Device ID'] == devideId) &
            (df['Location'] == location) &
            (df['Date'].dt.year == year) &
            (df['Date'].dt.month == month) &
            (df['Date'].dt.day == day)
        )

        filteredDf = df[mask]

        if not filteredDf.empty :
            # Debugging
            # print(f"{Fore.LIGHTBLACK_EX}{filteredDf}{Style.RESET_ALL}")
            plannedTime = filteredDf["Planned Time"]
            runTime = filteredDf["Run Time"]
            idealCycleTime = filteredDf["Ideal Cycle Time"]
            totalUnits = filteredDf["Total Units"]
            goodUnits = filteredDf["Good Units"]


            availability = runTime / plannedTime
            performance = (idealCycleTime * totalUnits) / runTime 
            quality = goodUnits / totalUnits

            oee = availability * performance * quality * 100

            return f"Availability: {round(availability, 4)}, Performance: {round(performance, 4)}, Quality: {round(quality, 4)}, OEE (%): {round(oee, 2)}"
        else:
            # If the device does not exist - give similar devices to the user.
            mask =  (
                (df['Date'].dt.year == year) &
                (df['Date'].dt.month == month) &
                (df['Date'].dt.day == day)
            )

            filterDf = df[mask]
            
            # Debugging
            # print(f"{Fore.LIGHTBLACK_EX}{filterDf}{Style.RESET_ALL}")

            return f"{filterDf}"
    
    except Exception as e:
        raise ValueError(f"{Fore.RED}Unexpected error during OEE calculation: {e}{Style.RESET_ALL}")
