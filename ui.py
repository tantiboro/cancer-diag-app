# ui.py
import streamlit as st
import pandas as pd
from typing import Dict

def create_input_form(data: pd.DataFrame) -> Dict[str, float]:
    """Creates the sidebar sliders and returns a dict of the user's input."""
    
    st.sidebar.header("Cell Nuclei Details")
    
    # List of all features
    slider_labels = [
        ("Radius (mean)", "radius_mean"), ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"), ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"), ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"), ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"), ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"), ("Texture (se)", "texture_se"), 
        ("Perimeter (se)", "perimeter_se"), ("Area (se)", "area_se"), 
        ("Smoothness (se)", "smoothness_se"), ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"), ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"), ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"), ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"), ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"), ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"), ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"), ("Fractal dimension (worst)", "fractal_dimension_worst")
    ]
    
    input_data = {}

    for label, col in slider_labels:
        input_data[col] = st.sidebar.slider(
            label=label, 
            min_value=float(data[col].min()), 
            max_value=float(data[col].max()), 
            value=float(data[col].mean()),
            step=float((data[col].max() - data[col].min()) / 100) # Add a reasonable step
        )
    
    return input_data