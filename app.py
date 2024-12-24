import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import os

# Import your custom UI/UX components
from ux import render_ui

def push_to_github(file_path, commit_message="Update lego.csv"):
    """
    Clones the GitHub repo, replaces lego.csv,
    commits, and pushes to the main branch.
    """
    token = st.secrets["GITHUB_TOKEN"]  # from secrets.toml
    username = "habdulhaq87"
    repo_name = "lego"

    # 1. Remove any existing temp_repo folder (clean slate)
    if os.path.exists("temp_repo"):
        subprocess.run(["rm", "-rf", "temp_repo"])

    # 2. Clone the repo into temp_repo
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    subprocess.run(["git", "clone", repo_url, "temp_repo"])

    # 3. Copy updated lego.csv to the cloned repo
    subprocess.run(["cp", file_path, "temp_repo/lego.csv"])

    # 4. Commit and push changes
    os.chdir("temp_repo")
    subprocess.run(["git", "config", "user.email", "bot@example.com"])
    subprocess.run(["git", "config", "user.name", "Streamlit Bot"])
    subprocess.run(["git", "add", "lego.csv"])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push", "origin", "main"])

    # 5. Return to parent folder and remove temp_repo
    os.chdir("..")
    subprocess.run(["rm", "-rf", "temp_repo"])


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
    st.sidebar.image("logo.jpg", use_container_width=True)
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

        # Use selectbox to choose from existing CSV values
        block_type = st.selectbox("Block Type", sorted(df["Block Type"].unique()))
        block_shape = st.selectbox("Block Shape", sorted(df["Block Shape"].unique()))
        dimension = st.selectbox("Dimensions", sorted(df["Dimensions"].unique()))
        block_color = st.selectbox("Block Color", sorted(df["Block Color"].unique()))

        # Number inputs for quantity fields
        available_quantity = st.number_input("Available Quantity", min_value=0, step=1)
        sold_out = st.number_input("Sold Out", min_value=0, step=1)

        # Button to add row to CSV + push to GitHub
        if st.button("Add Row"):
            # Read the current CSV into a DataFrame again to ensure consistency
            current_df = pd.read_csv("lego.csv")

            # Create a new row as a DataFrame
            new_row = pd.DataFrame({
                "Block Type": [block_type],
                "Block Shape": [block_shape],
                "Dimensions": [dimension],
                "Block Color": [block_color],
                "Available Quantity": [int(available_quantity)],
                "Sold Out": [int(sold_out)],
            })

            # Use pd.concat to append the new row
            updated_df = pd.concat([current_df, new_row], ignore_index=True)

            # Write updated data back to CSV
            updated_df.to_csv("lego.csv", index=False)

            # Attempt to push updated CSV to GitHub
            try:
                push_to_github("lego.csv", commit_message="Add new row to lego.csv")
                st.success("New data added and changes pushed to GitHub successfully!")
            except Exception as e:
                st.error(f"New data added locally, but GitHub push failed: {str(e)}")

            st.balloons()  # Fun effect

if __name__ == "__main__":
    main()
