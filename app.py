import streamlit as st
import pandas as pd
import altair as alt
from ux import render_ui  # Import your custom UX components

def main():
    # Set page configuration (including the logo as favicon)
    st.set_page_config(
        page_title="Lego Dataset Dashboard",
        page_icon="logo.jpg",  # This will be used as the favicon
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Display the logo at the top of the main page
    st.image("logo.jpg", width=80)
    st.title("Lego Dataset Visualization")

    # Display the logo and website link in the sidebar
    st.sidebar.image("logo.jpg", use_column_width=True)
    st.sidebar.markdown("[amas.com](https://amas.com)")

    # Load the dataset
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

    # Filtered DataFrame
    filtered_df = df[
        (df["Block Type"].isin(block_types)) &
        (df["Block Shape"].isin(block_shapes)) &
        (df["Block Color"].isin(block_colors))
    ]

    # Group data for charts
    grouped_data = filtered_df.groupby(
        ["Block Type", "Block Color"], as_index=False
    )[["Available Quantity", "Sold Out"]].sum()

    # Call the UX rendering function
    render_ui(df, filtered_df, grouped_data)

if __name__ == "__main__":
    main()
