import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="StrokeSense - Stroke Prediction App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set a dark theme for the entire app with red button
st.markdown("""
<style>
    /* Dark background for the entire app */
    .stApp {
        background-color: #121212;
        color: white;
    }

    /* All text in white */
    p, label, span, div, h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        color: white;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        opacity: 0.9;
    }

    /* Prediction boxes */
    .prediction-box {
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: bold;
    }

    .high-risk {
        background-color: #DC2626;
        color: white;
    }

    .low-risk {
        background-color: #059669;
        color: white;
    }

    /* Slider styling */
    .stSlider > div {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
    }

    .stSlider > div > div > div {
        background-color: #DC2626 !important;
    }

    /* Radio buttons and checkboxes */
    .stRadio label, .stCheckbox label {
        color: white !important;
    }

    /* Red button styling */
    .stButton > button {
        background-color: #DC2626 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-size: 1rem !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #B91C1C !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Section dividers */
    hr {
        border-color: #333333;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #DC2626 !important;
    }

    /* Markdown text */
    .stMarkdown {
        color: white;
    }

    /* Alert boxes */
    .stAlert {
        background-color: #1E1E1E;
        color: white;
    }

    /* Dataframe styling */
    .dataframe {
        color: white;
    }

    /* Widget labels */
    .stWidgetLabel {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>StrokeSense</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Stroke Risk Prediction Tool</p>", unsafe_allow_html=True)

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.write("## Patient Information")
    st.write("Please enter the patient's details below to predict stroke risk.")

    # Input fields with sliders for numeric values
    age = st.slider("Age", min_value=25, max_value=100, value=50, step=1,
                  help="Patient's age in years")

    gender = st.radio("Gender", ["Female", "Male"])
    gender_value = 0 if gender == "Female" else 1

    hypertension = st.checkbox("Hypertension")
    hypertension_value = 1 if hypertension else 0

    heart_disease = st.checkbox("Heart Disease")
    heart_disease_value = 1 if heart_disease else 0

    diabetes = st.checkbox("Diabetes")
    diabetes_value = 1 if diabetes else 0

    bmi = st.slider("BMI", min_value=15.0, max_value=45.0, value=25.0, step=0.1,
                  help="Body Mass Index (weight in kg / height in m²)")

    avg_glucose = st.slider("Average Glucose Level (mg/dL)",
                          min_value=45.0, max_value=175.0, value=100.0, step=1.0,
                          help="Average blood glucose level in mg/dL")

    # Red prediction button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Predict Stroke Risk"):
        # Prepare data for API call
        api_url = "https://stroke-prediction-app-335914011988.europe-west1.run.app/predict"

        params = {
            "Age": age,
            "Gender": gender_value,
            "Hypertension": hypertension_value,
            "Heart_Disease": heart_disease_value,
            "BMI": bmi,
            "Avg_Glucose": avg_glucose,
            "Diabetes": diabetes_value
        }

        try:
            # Make API call
            st.info("Connecting to API...")
            response = requests.get(api_url, params=params, timeout=5)

            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", 0)

                # Display prediction
                with col2:
                    st.write("## Prediction Result")

                    if prediction == 1:
                        st.markdown("<div class='prediction-box high-risk'><h3>High Risk of Stroke</h3><p>The model predicts that this patient has a high risk of stroke.</p></div>", unsafe_allow_html=True)
                        st.warning("Please consult with a healthcare professional for a thorough evaluation.")
                    else:
                        st.markdown("<div class='prediction-box low-risk'><h3>Low Risk of Stroke</h3><p>The model predicts that this patient has a low risk of stroke.</p></div>", unsafe_allow_html=True)
                        st.success("Continue monitoring health factors and maintain a healthy lifestyle.")

                    # Display risk factors
                    st.write("### Risk Factors Analysis")

                    risk_factors = []
                    if age > 65:
                        risk_factors.append("Advanced age (>65)")
                    if hypertension:
                        risk_factors.append("Hypertension")
                    if heart_disease:
                        risk_factors.append("Heart disease")
                    if diabetes:
                        risk_factors.append("Diabetes")
                    if bmi > 30:
                        risk_factors.append("Obesity (BMI > 30)")
                    if avg_glucose > 125:
                        risk_factors.append("High glucose levels")

                    if risk_factors:
                        st.write("Present risk factors:")
                        for factor in risk_factors:
                            st.write(f"- {factor}")
                    else:
                        st.write("No major risk factors identified.")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("""
            ⚠️ **API Connection Error**

            Could not connect to the API server. Please make sure your FastAPI server is running.

            For development purposes, you can use the mock prediction below:
            """)

            # Provide a mock prediction for development
            with col2:
                st.write("## Mock Prediction (API Offline)")
                mock_prediction = 1 if (age > 65 or hypertension or heart_disease or diabetes or bmi > 30 or avg_glucose > 125) else 0

                if mock_prediction == 1:
                    st.markdown("<div class='prediction-box high-risk'><h3>High Risk of Stroke (MOCK)</h3><p>This is a mock prediction since the API is offline.</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='prediction-box low-risk'><h3>Low Risk of Stroke (MOCK)</h3><p>This is a mock prediction since the API is offline.</p></div>", unsafe_allow_html=True)

                # Display risk factors
                st.write("### Risk Factors Analysis")

                risk_factors = []
                if age > 65:
                    risk_factors.append("Advanced age (>65)")
                if hypertension:
                    risk_factors.append("Hypertension")
                if heart_disease:
                    risk_factors.append("Heart disease")
                if diabetes:
                    risk_factors.append("Diabetes")
                if bmi > 30:
                    risk_factors.append("Obesity (BMI > 30)")
                if avg_glucose > 125:
                    risk_factors.append("High glucose levels")

                if risk_factors:
                    st.write("Present risk factors:")
                    for factor in risk_factors:
                        st.write(f"- {factor}")
                else:
                    st.write("No major risk factors identified.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Add information section
st.write("---")
st.write("## About Stroke Risk Factors")

st.write("""
Stroke is a serious medical condition that occurs when blood supply to part of the brain is interrupted or reduced,
preventing brain tissue from getting oxygen and nutrients. Brain cells begin to die within minutes.

### Common risk factors include:
- **Age**: Risk increases with age, especially after 55
- **Hypertension**: High blood pressure damages blood vessels
- **Heart Disease**: Various heart conditions can increase stroke risk
- **Diabetes**: Increases damage to blood vessels
- **BMI**: Obesity is linked to higher stroke risk
- **Glucose Levels**: High blood sugar can damage blood vessels
- **Gender**: Risk factors can affect men and women differently

### Disclaimer
This tool provides an estimate based on a machine learning model and should not replace professional medical advice.
Always consult with healthcare professionals for proper diagnosis and treatment.
""")

# Add a data visualization section
st.write("---")
st.write("## Stroke Risk Visualization")

# Create sample data for visualization
np.random.seed(42)
sample_size = 100
data = {
    'Age': np.random.normal(60, 15, sample_size),
    'BMI': np.random.normal(28, 5, sample_size),
    'Glucose': np.random.normal(110, 30, sample_size),
    'Stroke': np.random.choice([0, 1], size=sample_size, p=[0.8, 0.2])
}
df = pd.DataFrame(data)

# Set a color palette with good contrast
colors = ["#059669", "#DC2626"]  # Green for no stroke, red for stroke

# Set dark background for plots
plt.style.use('dark_background')

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Age vs. Stroke", "BMI vs. Stroke", "Glucose vs. Stroke"])

with tab1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Stroke', y='Age', data=df, ax=ax, palette=colors)
    ax.set_title('Age Distribution by Stroke Occurrence', fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('Stroke (0 = No, 1 = Yes)', fontsize=12, color='white')
    ax.set_ylabel('Age', fontsize=12, color='white')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    fig.patch.set_facecolor('#121212')
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Stroke', y='BMI', data=df, ax=ax, palette=colors)
    ax.set_title('BMI Distribution by Stroke Occurrence', fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('Stroke (0 = No, 1 = Yes)', fontsize=12, color='white')
    ax.set_ylabel('BMI', fontsize=12, color='white')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    fig.patch.set_facecolor('#121212')
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Stroke', y='Glucose', data=df, ax=ax, palette=colors)
    ax.set_title('Glucose Level Distribution by Stroke Occurrence', fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('Stroke (0 = No, 1 = Yes)', fontsize=12, color='white')
    ax.set_ylabel('Glucose Level', fontsize=12, color='white')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    fig.patch.set_facecolor('#121212')
    st.pyplot(fig)

# Footer
st.write("---")
st.markdown("<p style='text-align: center; color: white; opacity: 0.7;'>© 2023 StrokeSense | Developed for healthcare professionals</p>", unsafe_allow_html=True)
