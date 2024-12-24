import streamlit as st
import altair as alt

def render_ui(df, filtered_df, grouped_data):
    # Raw Data (collapsible)
    with st.expander("Raw Data", expanded=False):
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

    # Key Metrics
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

    # Filtered Data (collapsible)
    with st.expander("Filtered Data", expanded=True):
        st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True)

    # Tabs for charts
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

    st.write(
        """
        ---
        **Tip**: Use the sidebar to filter by Block Type, Shape, and Color.
        """
    )
