import pandas as pd
import streamlit as st

def filter_by_date_range(df: pd.DataFrame, date_column: str, date_range: tuple) -> pd.DataFrame:
    """
    Filters the DataFrame by a specified date range.

    :param df: The Pandas DataFrame to be filtered.
    :param date_column: The name of the column that contains the date values to filter by.
    :param date_range: A tuple containing the start and end date for filtering. If only one date is provided, 
                       the DataFrame will be filtered for that exact date.
    :return: A filtered DataFrame based on the specified date range.
    """
    if df.empty:
        print("⚠️ The DataFrame is empty. Returning without filtering.")
        return df

    if date_column not in df.columns:
        print(f"❌ The column '{date_column}' is not present in the DataFrame! Available columns: {df.columns.tolist()}")
        return df

    # Convert to datetime
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce").dt.date
    
    if len(date_range) < 2:
        df = df[df[date_column] == date_range[0]]
    else:
        df = df[(df[date_column] >= date_range[0]) & (df[date_column] <= date_range[1])]

    return df
