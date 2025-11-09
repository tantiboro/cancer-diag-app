# data_processing.py
import pandas as pd
import streamlit as st
from typing import Dict, Any

@st.cache_data
def get_clean_data(data_path: str) -> pd.DataFrame:
    """Loads and cleans the data from the specified path."""
    df = pd.read_csv(data_path)
    if 'id' in df.columns:
        df = df.drop(['id'], axis=1)
    if 'diagnosis' in df.columns:
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
    return df

def get_scaled_values_dict(values_dict: Dict[str, float], data: pd.DataFrame) -> Dict[str, float]:
    """
    Scales a dictionary of input values between 0 and 1 based on 
    the min/max of the columns in the provided DataFrame.
    """
    X = data.drop(['diagnosis'], axis=1)
    scaled_dict = {}

    for key, value in values_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        # Avoid division by zero if max == min
        if (max_val - min_val) > 0:
            scaled_value = (value - min_val) / (max_val - min_val)
        else:
            scaled_value = 0.5 # Default to middle
        scaled_dict[key] = scaled_value

    return scaled_dict