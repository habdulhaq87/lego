import streamlit as st
import pandas as pd
import altair as alt

# Import UI/UX elements from ux.py
from ux import render_ui

def main():
    # Configure the Streamlit page
    st.set_page_config(
        page_title="Lego Dataset Dashboard",
        page_icon="logo.jpeg",  # Optionally use the logo as the browser tab icon
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add a header with logo and link to amas.com
    # Using HTML/CSS to align logo and title horizontally
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 1rem;">
            <img src="logo.jpeg" alt="Logo" style="height: 60px;">
            <h2 style="margin-bottom: 0;">Lego Dataset Visualization</h2>
        </div>
        <p style="margin-top: 0;">
            Brought to you by <a href="https://amas.com" target="_blank">amas.com</a>
        </p>
        <hr style="margin: 1rem 0;">
        """,
        unsafe_allow_html=True
    )

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

    # Filter the data
    filtered_df = df[
        (df["Block Type"].isin(block_types)) &
        (df["Block Shape"].isin(block_shapes)) &
        (df["Block Color"].isin(block_colors))
    ]

    # Group data for charts
    grouped_data = filtered_df.groupby(
        ["Block Type", "Block Color"], as_index=False
    )[["Available Quantity", "Sold Out"]].sum()

    # Render the rest of the UI (from ux.py)
    render_ui(df, filtered_df, grouped_data)

if __name__ == "__main__":
    main()
