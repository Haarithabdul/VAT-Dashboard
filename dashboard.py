#DEPENDENCIES
import pandas as pd
import dashboardLogic as dl
import classFile
import fileMap
import streamlit as sl
import plotly.express as px


def initDashboard(quarters):
    #Sets title and widens the page layout
    sl.title("VAT Returns Dashboard")

    sl.set_page_config(layout="wide")

    #Creates a select box to choose which financial quarter they want to display
    quarterSelect = sl.sidebar.selectbox(
        "Select a Quarter(s):",
        quarters
    )

    #Button on the sidebar to show data for selected quarter, runs error checks
    if sl.sidebar.button("Display"):
        if quarterSelect is None:
            sl.write("Please select a value")
        else:
            #Maintains selected quarter after other controls are selected
            sl.session_state["quarterSelect"] = quarterSelect
            return quarterSelect

    return sl.session_state.get("quarterSelect", None)


def createColumn1(col1, df):
    #Creates var for total net liability of all BU's
    total_net_liability = round(dl.calcTotalNetLiabilities(df), 2)

    with col1:
        with sl.container():
            #Displays total net liability as a metric
            sl.metric(
                label="Total Net Liability",
                value=f'£ {total_net_liability}'
            )

        with sl.container():
            #Allows user to select any BU's
            select_BU = sl.multiselect(
                "BU's:",
                df["Group member/Unit"],
                key="col1_select_BU"
            )

            #Adds total as a new column and sorts
            df["Total Net Liability"] = total_net_liability

            df = df.sort_values("Net Liability", ascending=False)

            grouped_df = df[["Group member/Unit", "Net Liability", "Total Net Liability"]]

            #Filters dataframe by selected BU is there is a value present
            if select_BU:
                grouped_df = dl.filterByUnit(grouped_df, select_BU, "list")

            #Creates and displays bar chart
            figure = px.bar(grouped_df,
                            x="Total Net Liability",
                            y="Net Liability",
                            color="Group member/Unit",
                            title="Total Net Liability per BU")

            sl.plotly_chart(figure, use_container_width=True)



def createColumn2(col2, df, quarter, col3):
    #Allows user to selected time range they want to compart data to
    select_period = sl.sidebar.segmented_control(
        "Time Period",
        options=[3, 6, 12, 18],
        default=6
    )

    with col2:
        if select_period != 0:
            if select_period in (6, 12, 18):
                graphQuarters = dl.sliceQuarterList(quarter, select_period)

                #Creates an extended dataframe from previous data
                extended_df = dl.extendDataFrame(graphQuarters)

                figure = px.line(
                    x=extended_df["Quarter"],
                    y=extended_df["Total Net Liability"],
                    title=f"Trend Net Liability over {select_period} months"
                )

                figure.update_xaxes(title_text="Quarter")
                figure.update_yaxes(title_text="Total Net Liability")

                #Creates and plots a line graph
                sl.plotly_chart(figure, use_container_width=False)

        else:
            sl.write("Select a time period (Previous months)")

        with sl.container():
            figure = px.pie(
                names=df["Group member/Unit"],
                values=df["Net Liability"],
                title="Net Liability/BU"
            )

            #Creates and plots a pie chart
            sl.plotly_chart(figure, use_container_width=False)

    createColumn3(col3, extended_df)


def createColumn3(col3, extended_df):
    #Seperate BU select for third column
    with col3:
        select_BU = sl.selectbox(
            "BU's:",
            extended_df["Group member/Unit"].unique(),
            key="col3_select_BU"
        )

        with sl.container():
            #Filter dataframe by selected BU's
            filtered_df = dl.filterByUnit(extended_df, select_BU, "single")

            figure = px.bar(
                filtered_df,
                x=filtered_df["Quarter"],
                y=filtered_df["Net Liability"],
                title=f"{select_BU} Change in Net Liability"
            )

            #Creates and plots a bar chart to compare single BU between quarters
            sl.plotly_chart(figure, use_container_width=True)

            #Calculates difference between most and least recent quarter to check if its a repayment/liability
            difference = filtered_df["Net Liability"].iloc[-1] - filtered_df["Net Liability"].iloc[0]

            #Displays difference and shows number in green/red is repayment/liability
            sl.metric(
                label="Net Liability Change (First --> Last Quarter)",
                value=f"£{difference:,.2f}",
                delta=f"{difference:,.2f}",
                delta_color="inverse"
            )


def createDashboard(quarter, filesDict):
    #Creates dataframe for selected file, and columns for organisation and formatting
    df = dl.createDataFrame(quarter, filesDict)

    column1, column2, column3 = sl.columns(3)

    createColumn1(column1, df)
    createColumn2(column2, df, quarter, column3)


def main():
    quarterSelect = initDashboard(fileMap.quarters)

    if quarterSelect is not None:
            createDashboard(quarterSelect, fileMap.filesDict)


if __name__ == "__main__":
    main()