import streamlit as st
import pandas as pd

def sidebar_filters(motel_df: pd.DataFrame, date_df: pd.DataFrame) -> tuple:
    """
    Creates interactive filters in the sidebar, allowing selection of date ranges.

    :param motel_df: A Pandas DataFrame containing information about motels with columns 'motel_name' and 'motel_id'.
    :param date_df: A Pandas DataFrame containing session and analysis dates with columns 'session_created_at' 
                    and 'analysis_created_at'.
    :return: A tuple containing the selected motel ID, the selected date range for analysis, 
             and the selected date range for sessions.
    """
    st.sidebar.title("Filters")

    # Create a dictionary of options for the selectbox
    motel_options = {"All": None}  # Default option
    motel_options.update(dict(zip(motel_df["motel_name"], motel_df["motel_id"])))

    # Motel selection
    selected_motel_name = st.sidebar.selectbox("Choose the Motel", list(motel_options.keys()))
    selected_motel_id = motel_options[selected_motel_name]

    # Session date range selection
    selected_session_date_range = st.sidebar.date_input(
        "Select the Session Date Range",
        value=[date_df['session_created_at'].min(), date_df['session_created_at'].max()],  # Initial range
        min_value=date_df["session_created_at"].min(),
        max_value=date_df["session_created_at"].max(),
        format="DD.MM.YYYY"
    )

    # Analysis date range selection
    selected_analysis_date_range = st.sidebar.date_input(
        "Select the Analysis Date Range",
        value=[date_df['analysis_created_at'].min(), date_df['analysis_created_at'].max()],  # Initial range
        min_value=date_df["analysis_created_at"].min(),
        max_value=date_df["analysis_created_at"].max(),
        format="DD.MM.YYYY"
    )

    return selected_motel_id, selected_analysis_date_range, selected_session_date_range