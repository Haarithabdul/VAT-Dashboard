#DEPENDENCIES
from dashboardLogic import calcTotalNetLiabilities, filterByUnit, createDataFrame, sliceQuarterList, extendDataFrame
import pytest
import pandas as pd


@pytest.fixture
def test_df():
    return pd.DataFrame({
        "Group member/Unit": ["BU1", "BU2", "BU3"],
        "Net Liability": [100, -50, 200]
    })

@pytest.fixture
def test_quarters():
    return [
        "Q1-2023", "Q2-2023", "Q3-2023", "Q4-2023/24"
        ]

@pytest.fixture
def test_filesDict(test_quarters):
    return {
    test_quarters[0]: "Dummy Q1-2023.xlsx",
    test_quarters[1]: "Dummy Q2-2023.xlsx",
    test_quarters[2]: "Dummy Q3-2023.xlsx",
    test_quarters[3]: "fileWontFind"
    }


def test_calcTotalNetLiabilities(test_df):
    assert calcTotalNetLiabilities(test_df) == 250


def test_filterByUnit(test_df):
    filtered_df = filterByUnit(test_df, "BU2", "single")
    assert len(filtered_df) == 1

    filtered_df = filterByUnit(test_df, ["BU2", "BU3"], "list")
    assert len(filtered_df) == 2

    with pytest.raises(ValueError):
        filtered_df = filterByUnit(test_df, ["BU1", "BU2", "BU3"], "single")
        assert filtered_df == None


def test_createDataFrame(test_df, test_quarters, test_filesDict):
    testFrame = createDataFrame(test_quarters[0], test_filesDict)
    assert isinstance(testFrame, pd.DataFrame)

    testFrame = createDataFrame(test_quarters[3], test_filesDict)
    assert testFrame == None


def test_sliceQuarterList(test_quarters):
    quarter = "Q4-2023/24"
    timeRange = 12

    sliced = sliceQuarterList(quarter, timeRange)

    assert sliced == test_quarters

def test_extendDataFrame(test_quarters):
    test_extended_df = extendDataFrame(test_quarters)

    assert len(test_extended_df) == 164