# model.py
import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Any
import pandas as pd

@st.cache_resource
def get_model(df: pd.DataFrame) -> Tuple[LogisticRegression, StandardScaler]:
    """Trains and returns the model and scaler."""
    
    # Separate features and target
    X = df.drop(['diagnosis'], axis=1)
    y = df['diagnosis']

    # Scale predictors
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # (Optional) Print test metrics to console during dev
    y_pred = model.predict(X_test)
    print("Model Accuracy: ", accuracy_score(y_test, y_pred))
    # print("Classification report: \n", classification_report(y_test, y_pred))

    return model, scaler

def display_predictions(input_data: dict, model: LogisticRegression, scaler: StandardScaler):
    """Takes user input data and displays the model's prediction."""
    
    # Convert dict to numpy array and scale it
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_data_scaled = scaler.transform(input_array)

    st.subheader('Cell Cluster Prediction')
    st.write("The cell cluster is: ")

    prediction = model.predict(input_data_scaled)
    proba = model.predict_proba(input_data_scaled)[0]

    if prediction[0] == 0:
        st.write("<span class='diagnosis bright-green'>Benign</span>", unsafe_allow_html=True)
        st.write(f"**Probability of being benign:** {proba[0]:.2%}")
        st.write(f"**Probability of being malignant:** {proba[1]:.2%}")
    else:
        st.write("<span class='diagnosis bright-red'>Malignant</span>", unsafe_allow_html=True)
        st.write(f"**Probability of being malignant:** {proba[1]:.2%}")
        st.write(f"**Probability of being benign:** {proba[0]:.2%}")

    st.caption("This app can assist medical professionals, but should not substitute professional diagnosis.")