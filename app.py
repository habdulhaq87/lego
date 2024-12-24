import streamlit as st
import pandas as pd
from ux import render_ui
import altair as alt

def main():
    # Set page config
    st.set_page_config(
        page_title="Lego Dataset Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Lego Dataset Visualization")

    # Load dataset
    df = pd.read_csv("lego.csv")

    # -------------------------
    # Sidebar Filters
    # -------------------------
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

    # Filter the data
    filtered_df = df[
        (df["Block Type"].isin(block_types)) &
        (df["Block Shape"].isin(block_shapes)) &
        (df["Block Color"].isin(block_colors))
    ]

    # Grouped data for charts
    grouped_data = filtered_df.groupby(
        ["Block Type", "Block Color"], as_index=False
    )[["Available Quantity", "Sold Out"]].sum()

    # Render the UI components
    render_ui(df, filtered_df, grouped_data)

if __name__ == "__main__":
    main()
