#DEPENDENCIES
import fileMap
import classFile
import pandas as pd
import streamlit as sl


#Sums and returns total for net liability
def calcTotalNetLiabilities(df):
    return df["Net Liability"].sum()


#Quickly filters dataframe by BU, different syntax whether it's a list or not
def filterByUnit(df, select_BU, type):
    if type == "list":
        return df.loc[df["Group member/Unit"].isin(select_BU)]
    elif type == "single":
        return df.loc[df["Group member/Unit"] == select_BU]


def createDataFrame(quarter, filesDict):
    #Creates and cleans dataframe using class from classFile
    try:
        newData = classFile.Data(quarter, filesDict)
        df = newData.convertToDataFrame()

        return df

    except FileNotFoundError:
        sl.write("No available file to read")
    except KeyError:
        pass
    except Exception as e:
        print(f"Error: {e}")


def sliceQuarterList(quarter, timeRange):
    # Maps how many quarters to go back based on month range selected
    monthsToQuarterDict = {
        3: 1,
        6: 2,
        12: 4,
        18: 6
    }

    quarterList = fileMap.quarters

    # Gets index of currently selected quarter
    currentQuarterIndex = quarterList.index(quarter)

    #Calculates index and creates a slice of the full list
    startIndex = max(0, currentQuarterIndex - monthsToQuarterDict[timeRange])
    graphQuarters = quarterList[startIndex: currentQuarterIndex + 1]

    return graphQuarters


def extendDataFrame(graphQuarters):
    dfs = []

    #For each quarter, creates a new dataframe, adds to list, adds new columns
    for quart in graphQuarters:
        new_df = createDataFrame(quart, fileMap.filesDict)

        new_df = new_df.copy()

        new_df["Total Net Liability"] = calcTotalNetLiabilities(new_df)
        new_df["Quarter"] = quart

        dfs.append(new_df)

    #Combines all dataframes in list and stops repeating indexes
    extended_df = pd.concat(dfs, ignore_index=True)

    return extended_df