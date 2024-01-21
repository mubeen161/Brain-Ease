import streamlit as st
import pickle
import numpy as np
from PIL import Image
model_filename11 = 'human_stress_model.pkl'  # Replace with the actual filename
with open(model_filename11, 'rb') as file:
    model1 = pickle.load(file)

def predict_stress_level(inputss):
    inputss = np.array(inputss).reshape(1, -1)
    prediction1 = model1.predict(inputss)
    return prediction1[0]

def stress_pred():
    st.title("Stress Level Prediction")
    
    image = Image.open('moderate stress.png')
    st.image(image)
    
    st.markdown("""
        <style>
        .big-font {
            font-size:50px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font">Enter the following inputs to predict stress level:</p>', unsafe_allow_html=True)
    
    # Input fields
    name = st.text_input("Name ")
    age = st.selectbox("Gender", ('Male', 'Female', 'Others'))
    sr = st.slider("Snoring Rate (Snoring frequency/total sleep time)", min_value=0.0, max_value=100.0, step=0.1)
    rr = st.slider("Respiration Rate (no. of breaths/min)", min_value=5.0, max_value=50.0, step=0.1)
    t = st.slider("Body Temperature (in F)", min_value=85.0, max_value=110.0, step=0.1)
    bo = st.slider("Blood Oxygen (in %)", min_value=70.0, max_value=100.0, step=0.1)
    sr_1 = st.slider("Sleeping Hours", min_value=0.0, max_value=24.0, step=0.5)
    hr = st.slider("Heart Rate", min_value=40.0, max_value=90.0, step=0.1)
    
    st.markdown("""
        <style>
        .op-font {
            font-size:10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Predict button
    if st.button("Predict Stress Level"):
        inputs = [sr, rr, t, bo, sr_1, hr]
        predicted_sl = predict_stress_level(inputs)
        if predicted_sl == 0:
            st.markdown('<p class="op-font">Minimal Stress:</p>', unsafe_allow_html=True)
            st.text("Occasional moments of mild tension or discomfort")
            image1 = Image.open('stress 1.0.png')
            st.image(image1)
        elif predicted_sl == 1:
            st.markdown('<p class="op-font">Mild Stress: </p>', unsafe_allow_html=True)
            st.text("Feeling a bit on edge, but you can still handle things")
            image2 = Image.open('stress 2.png')
            st.image(image2)
        elif predicted_sl == 2:
            st.markdown('<p class="op-font">Moderate Stress: </p>', unsafe_allow_html=True)
            st.text("Multiple deadlines & complex tasks require heightened concentration & adaptive problem solving ")
            image3 = Image.open('stress 1.png')
            st.image(image3)
        elif predicted_sl == 3:
            st.markdown('<p class="op-font">High Stress:</p>', unsafe_allow_html=True)
            st.text(" Pressure builds up, messing with your concentration and ability to unwind. ")
            image4 = Image.open('stress 4.png')
            st.image(image4)
        else:
            st.markdown('<p class="op-font">Severe Stress: </p>', unsafe_allow_html=True)
            st.text("Experiencing profound tension significantly impairs cognitive function & emotional well-being , severe health ramifications emphasizing the urgent need for help to reduce health effects ")
            image5 = Image.open('stress 5.png')
            st.image(image5)


if __name__ == '__main__':
    stress_pred()
    
