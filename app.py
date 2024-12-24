import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.title("Lego Dataset Visualization")

    # Load the dataset
    df = pd.read_csv("lego.csv")

    # Display the raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Create sidebar filters
    st.sidebar.header("Filter Options")
    block_types = st.sidebar.multiselect(
        "Select Block Type(s)",
        options=df["Block Type"].unique(),
        default=df["Block Type"].unique()
    )
    block_shapes = st.sidebar.multiselect(
        "Select Block Shape(s)",
        options=df["Block Shape"].unique(),
        default=df["Block Shape"].unique()
    )
    block_colors = st.sidebar.multiselect(
        "Select Block Color(s)",
        options=df["Block Color"].unique(),
        default=df["Block Color"].unique()
    )

    # Apply the filters to the DataFrame
    filtered_df = df[
        (df["Block Type"].isin(block_types)) &
        (df["Block Shape"].isin(block_shapes)) &
        (df["Block Color"].isin(block_colors))
    ]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Group the filtered data to visualize total Available vs. Sold Out
    grouped_data = filtered_df.groupby(["Block Type", "Block Color"], as_index=False)[
        ["Available Quantity", "Sold Out"]
    ].sum()

    # Create a bar chart showing Available Quantity
    st.subheader("Total Available Quantity by Block Type & Color")
    available_chart = (
        alt.Chart(grouped_data)
        .mark_bar()
        .encode(
            x="Block Type:N",
            y="Available Quantity:Q",
            color="Block Color:N",
            tooltip=["Block Type", "Block Color", "Available Quantity", "Sold Out"]
        )
        .properties(width=600)
    )
    st.altair_chart(available_chart, use_container_width=True)

    # Create a bar chart showing Sold Out
    st.subheader("Total Sold Out by Block Type & Color")
    sold_out_chart = (
        alt.Chart(grouped_data)
        .mark_bar()
        .encode(
            x="Block Type:N",
            y="Sold Out:Q",
            color="Block Color:N",
            tooltip=["Block Type", "Block Color", "Available Quantity", "Sold Out"]
        )
        .properties(width=600)
    )
    st.altair_chart(sold_out_chart, use_container_width=True)

if __name__ == "__main__":
    main()
