# app.py
import streamlit as st
import pandas as pd

# Import your modules
import data_processing
import model
import plotting
import ui

# --- Constants ---
DATA_PATH = './data/data.csv'
STYLE_PATH = './assets/style.css'

def load_css(file_path: str):
    """Loads a CSS file and injects it into the app."""
    try:
        with open(file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at {file_path}. Styling will be default.")

def create_app():
    """Builds the full Streamlit application."""
    
    st.set_page_config(
        page_title="Breast Cancer Diagnosis",
        page_icon=":female-doctor:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css(STYLE_PATH)

    st.title("Breast Cancer Diagnosis")
    st.write("This app predicts whether a breast mass is benign or malignant based on measurements from a cytology lab. "
             "Update the measurements by hand using the sliders in the sidebar.")

    # --- Load Data and Model (Cached) ---
    data = data_processing.get_clean_data(DATA_PATH)
    ml_model, scaler = model.get_model(data)

    # --- Sidebar ---
    input_data = ui.create_input_form(data)

    # --- Body ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Scale data for radar chart
        scaled_input = data_processing.get_scaled_values_dict(input_data, data)
        radar_chart = plotting.create_radar_chart(input_data, scaled_input)
        st.plotly_chart(radar_chart, use_container_width=True)
    
    with col2:
        model.display_predictions(input_data, ml_model, scaler)

    st.divider()

    # --- Data Visualization Section (UPDATED) ---
    with st.container():
        st.header("Data Visualization")

        # --- NEW PLOT ---
        with st.expander("Show Key Feature Distributions"):
            # Add the new box plot
            dist_chart = plotting.plot_feature_distributions(data)
            st.plotly_chart(dist_chart, use_container_width=True)

        # --- Original SPLOM Plot ---
        with st.expander("Show Full Scatterplot Matrix (SPLOM)"):
            splom_chart = plotting.plot_splom(data)
            st.plotly_chart(splom_chart, use_container_width=True)

def main():
    create_app()

if __name__ == '__main__':
    main()