#DEPENDENCIES
from pathlib import Path

base_dir = Path(__file__).parent

quarters = [
        "Q1-2023", "Q2-2023", "Q3-2023", "Q4-2023/24",
        "Q1-2024", "Q2-2024", "Q3-2024", "Q4-2024/25",
        "Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025/26"
    ]

filesDict = {
    quarters[0]: base_dir / "Dummy Q1-2023.xlsx",
    quarters[1]: base_dir / "Dummy Q2-2023.xlsx",
    quarters[2]: base_dir / "Dummy Q3-2023.xlsx",
    quarters[3]: base_dir / "Dummy Q4-2023.xlsx",
    quarters[4]: base_dir / "Dummy Q1-2024.xlsx",
    quarters[5]: base_dir / "Dummy Q2-2024.xlsx",
    quarters[6]: base_dir / "Dummy Q3-2024.xlsx",
    quarters[7]: base_dir / "Dummy Q4-2024.xlsx",
    quarters[8]: base_dir / "Dummy Q1-2025.xlsx",
    quarters[9]: base_dir / "Dummy Q2-2025.xlsx",
    quarters[10]: base_dir / "Dummy Q3-2025.xlsx",
    quarters[11]: base_dir / "Dummy Q4-2025.xlsx"
    }

#Code for looping through directory and building dictionary dynamically

'''
def createDict():
    folder = Path(r"D:\WORK\VAT Dashboard\VAT Reports")

    fileList = []
    filesDict = {}

    for file in folder.glob("VAT Controller_Report_*.xlsx"):
        fileList.append(file.name)

    for fileIter in range(len(fileList)):
        filesDict[quarters[fileIter]] = fileList[fileIter]

    return filesDict

filesDict = createDict()
'''