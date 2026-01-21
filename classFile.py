#DEPENDENCIES
from pathlib import Path
import pandas as pd


class Data:
    def __init__(self, quarter, filesDict):
        BASE_DIR = Path(__file__).parent
        DATA_FILE = BASE_DIR / filesDict[quarter]

        #Reads excel file given and specific sheet name
        self.rawData = pd.read_excel(DATA_FILE, sheet_name="Group detail")

    #Converts given file into a dataframe and renames columns
    def convertToDataFrame(self):
        dataFrame = pd.DataFrame(self.rawData)

        dataFrame = dataFrame.rename(columns={
            "Box 1": "VAT on Sales",
            "Box 3": "VAT on Purchases",
            "Box 5": "Net Liability",
            "Box 6": "Net Sales",
            "Box 7": "Net Purchases"
        })

        #Removes unneeded columns
        dataFrame = self.cleanFrame(dataFrame)

        return dataFrame

    def cleanFrame(self, dataFrame):
        dataFrame = dataFrame.drop(columns=["Box 2", "Box 4", "Box 8", "Box 9"])

        return dataFrame