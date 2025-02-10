import streamlit as st
from requests import get
from requests.exceptions import RequestException
import pandas as pd


from config import global_settings


@st.cache_data(ttl=global_settings.CACHE_VALID_DURATION)
def get_analysis() -> pd.DataFrame:
    """
    Fetches the analysis data from the backend and returns the response JSON with caching.

    This function caches the response for a specified duration to improve performance.

    :return: A Pandas DataFrame containing the analysis data.
    """
    return fetch_analysis()

def sync_analysis() -> pd.DataFrame:
    """
    Forces a refresh of the analysis data by clearing the cache and fetching the data again.

    This function clears the cache and calls the `fetch_analysis` function to retrieve the latest data.

    :return: A Pandas DataFrame containing the updated analysis data.
    """
    st.cache_data.clear()
    return fetch_analysis()

def fetch_analysis() -> pd.DataFrame:
    """
    Helper function to fetch data from the API.

    This function makes an HTTP GET request to the backend, handles errors, and converts the response to a DataFrame.

    :return: A Pandas DataFrame containing the fetched data, or None if an error occurs.
    """
    try:
        res = get(f"{global_settings.BACKEND_URL}/analysis", timeout=10)
        res.raise_for_status()
        res_json = res.json()
        
        df = pd.DataFrame(res_json)
                
        return df
    except RequestException as e:
        st.error(f"Error fetching analysis: {e}")
        return None