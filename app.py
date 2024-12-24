import streamlit as st
import pandas as pd
import altair as alt

# Import your custom UI/UX components
from ux import render_ui

def main():
    # Set page configuration (including the logo as favicon)
    st.set_page_config(
        page_title="Lego Dataset Dashboard",
        page_icon="logo.jpg",  # Used as the favicon
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Display the logo at the top of the main page
    st.image("logo.jpg", width=80)
    st.title("Lego Dataset Visualization")

    # Display the logo and website link in the sidebar
    st.sidebar.image("logo.jpg", use_column_width=True)
    st.sidebar.markdown("[amas.com](https://amas.com)")

    # -- Load the dataset once at startup --
    df = pd.read_csv("lego.csv")

    # -- Create tabs: Overview (with data visualization) and Add Data --
    tab_overview, tab_data_entry = st.tabs(["Overview", "Add Data"])

    # -------------------------
    # OVERVIEW TAB
    # -------------------------
    with tab_overview:
        st.subheader("Dataset Overview and Visualizations")

        # Sidebar Filters
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

        # Render the main UI (tables, metrics, charts)
        render_ui(df, filtered_df, grouped_data)

    # -------------------------
    # ADD DATA TAB
    # -------------------------
    with tab_data_entry:
        st.subheader("Add New Data to lego.csv")

        # Input fields for new data
        block_type = st.text_input("Block Type")
        block_shape = st.text_input("Block Shape")
        dimension = st.text_input("Dimensions")
        block_color = st.text_input("Block Color")
        available_quantity = st.number_input("Available Quantity", min_value=0, step=1)
        sold_out = st.number_input("Sold Out", min_value=0, step=1)

        # Button to add row to CSV
        if st.button("Add Row"):
            if block_type and block_shape and dimension and block_color:
                # Read the current CSV into a DataFrame
                current_df = pd.read_csv("lego.csv")

                # Create a new row as a dictionary
                new_row = {
                    "Block Type": block_type,
                    "Block Shape": block_shape,
                    "Dimensions": dimension,
                    "Block Color": block_color,
                    "Available Quantity": int(available_quantity),
                    "Sold Out": int(sold_out),
                }

                # Append the new row to the DataFrame
                current_df = current_df.append(new_row, ignore_index=True)

                # Write updated data back to CSV
                current_df.to_csv("lego.csv", index=False)

                st.success("New data added successfully!")
            else:
                st.error("Please fill in all required fields to add new data.")

if __name__ == "__main__":
    main()
