# plotting.py
import plotly.graph_objects as go
import plotly.express as px  # <-- Import Plotly Express
import pandas as pd
from typing import Dict

def plot_splom(df: pd.DataFrame) -> go.Figure:
    """Creates the Scatterplot Matrix (SPLOM)."""
    
    fig = go.Figure(data=go.Splom(
        dimensions=[
            dict(label='Radius (mean)', values=df['radius_mean']),
            dict(label='Texture (mean)', values=df['texture_mean']),
            dict(label='Perimeter (mean)', values=df['perimeter_mean']),
            dict(label='Area (mean)', values=df['area_mean']),
            dict(label='Smoothness (mean)', values=df['smoothness_mean']),
            dict(label='Compactness (mean)', values=df['compactness_mean']),
            dict(label='Concavity', values=df['concavity_mean']),
            dict(label='Concavity Points (mean)', values=df['concave points_mean']),
            dict(label='Symmetry (mean)', values=df['symmetry_mean']),
            dict(label='Fractal dimension (mean)', values=df['fractal_dimension_mean'])
        ],
        showupperhalf=False,
        marker=dict(
            color=df['diagnosis'],
            size=5,
            colorscale='Bluered',
            line=dict(width=0.5, color='rgb(230,230,230)')
        ),
        diagonal=dict(visible=False)
    ))

    title = "Scatterplot Matrix (SPLOM) for Breast Cancer Dataset"
    fig.update_layout(
        title=title,
        dragmode='select',
        width=1200,
        height=1000,
        hovermode='closest',
        autosize=True
    )
    return fig

# --- NEW FUNCTION ---
def plot_feature_distributions(df: pd.DataFrame) -> go.Figure:
    """
    Creates box plots to show the distribution of key features 
    for Benign vs. Malignant diagnoses.
    """
    
    # Map 0/1 back to Benign/Malignant for clearer labels
    df_plot = df.copy()
    df_plot['Diagnosis'] = df_plot['diagnosis'].map({0: 'Benign', 1: 'Malignant'})
    
    # We select a few key features to plot
    features_to_plot = ['radius_mean', 'texture_mean', 'compactness_mean', 'concavity_mean']
    
    
    fig = px.box(
        df_plot,
        y=features_to_plot,
        x='Diagnosis',
        color='Diagnosis',
        color_discrete_map={'Benign': '#00CC96', 'Malignant': '#EF553B'},
        title="Distribution of Key Features by Diagnosis",
        facet_col='variable', # Creates a separate plot for each feature
        facet_col_wrap=2,     # Wraps the plots into 2 columns
        height=700
    )
    
    # Clean up the y-axis titles (which are 'variable' by default)
    fig.update_yaxes(title=None, matches=None)
    # Make sure the x-axis title ('Diagnosis') is only shown at the bottom
    fig.update_xaxes(title='Diagnosis', showticklabels=True)
    # Clean up the facet titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    return fig
# --- END NEW FUNCTION ---


def create_radar_chart(input_data: Dict[str, float], scaled_data: Dict[str, float]) -> go.Figure:
    """Creates the radar chart for the 3 feature groups (mean, se, worst)."""
    
    # Note: Using scaled_data for the r-values so they fit on the 0-1 axis
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=[scaled_data['radius_mean'], scaled_data['texture_mean'], scaled_data['perimeter_mean'],
               scaled_data['area_mean'], scaled_data['smoothness_mean'], scaled_data['compactness_mean'],
               scaled_data['concavity_mean'], scaled_data['concave points_mean'], scaled_data['symmetry_mean'],
               scaled_data['fractal_dimension_mean']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points', 'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Mean'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[scaled_data['radius_se'], scaled_data['texture_se'], scaled_data['perimeter_se'], scaled_data['area_se'],
               scaled_data['smoothness_se'], scaled_data['compactness_se'], scaled_data['concavity_se'],
               scaled_data['concave points_se'], scaled_data['symmetry_se'], scaled_data['fractal_dimension_se']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points', 'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Standard Error'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[scaled_data['radius_worst'], scaled_data['texture_worst'], scaled_data['perimeter_worst'],
               scaled_data['area_worst'], scaled_data['smoothness_worst'], scaled_data['compactness_worst'],
               scaled_data['concavity_worst'], scaled_data['concave points_worst'], scaled_data['symmetry_worst'],
               scaled_data['fractal_dimension_worst']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points', 'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Worst'
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]  # Values are scaled, so range is 0-1
            )
        ),
        showlegend=True,
        autosize=True
    )
    
    return fig