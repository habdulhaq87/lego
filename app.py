import streamlit as st
import pandas as pd
import altair as alt

def main():
    # Set page configuration for a cleaner layout
    st.set_page_config(
        page_title="Lego Dataset Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Lego Dataset Visualization")

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

    # Apply the filters to the DataFrame
    filtered_df = df[
        (df["Block Type"].isin(block_types)) &
        (df["Block Shape"].isin(block_shapes)) &
        (df["Block Color"].isin(block_colors))
    ]

    # -------------------------
    # Data Overview (Collapsible)
    # -------------------------
    with st.expander("Raw Data", expanded=False):
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

    # -------------------------
    # Key Metrics
    # -------------------------
    st.subheader("Key Metrics")
    total_available = int(filtered_df["Available Quantity"].sum())
    total_sold_out = int(filtered_df["Sold Out"].sum())
    unique_types = len(filtered_df["Block Type"].unique())
    unique_colors = len(filtered_df["Block Color"].unique())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Available", total_available)
    col2.metric("Total Sold Out", total_sold_out)
    col3.metric("Block Types (Filtered)", unique_types)
    col4.metric("Block Colors (Filtered)", unique_colors)

    # -------------------------
    # Display Filtered Data (Collapsible)
    # -------------------------
    with st.expander("Filtered Data", expanded=True):
        st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True)

    # -------------------------
    # Grouped Data for Charts
    # -------------------------
    grouped_data = filtered_df.groupby(
        ["Block Type", "Block Color"], as_index=False
    )[["Available Quantity", "Sold Out"]].sum()

    # -------------------------
    # Tabs for Charts
    # -------------------------
    tab1, tab2 = st.tabs(["Available Quantity", "Sold Out"])

    with tab1:
        st.subheader("Total Available Quantity by Block Type & Color")
        available_chart = (
            alt.Chart(grouped_data)
            .mark_bar()
            .encode(
                x=alt.X("Block Type:N", sort=None),
                y="Available Quantity:Q",
                color="Block Color:N",
                tooltip=[
                    "Block Type",
                    "Block Color",
                    "Available Quantity",
                    "Sold Out"
                ]
            )
            .properties(width="container", height=400)
            .interactive()
        )
        st.altair_chart(available_chart, use_container_width=True)

    with tab2:
        st.subheader("Total Sold Out by Block Type & Color")
        sold_out_chart = (
            alt.Chart(grouped_data)
            .mark_bar()
            .encode(
                x=alt.X("Block Type:N", sort=None),
                y="Sold Out:Q",
                color="Block Color:N",
                tooltip=[
                    "Block Type",
                    "Block Color",
                    "Available Quantity",
                    "Sold Out"
                ]
            )
            .properties(width="container", height=400)
            .interactive()
        )
        st.altair_chart(sold_out_chart, use_container_width=True)

    # -------------------------
    # Additional Suggestions or Notes
    # -------------------------
    st.write(
        """
        ---
        **Tip**: Use the sidebar to filter by Block Type, Shape, and Color.
        """
    )

if __name__ == "__main__":
    main()
