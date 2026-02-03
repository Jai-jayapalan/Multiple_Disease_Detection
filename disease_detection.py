from tensorflow.keras.models import load_model
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import os
import re
from braintumorchk import getResult
from alzemirchk import alzeimerckh
from pneumoniachk import predict_image
from sndemail import send_email, sends_email

# --- Helper Functions ---

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_mobile(phone):
    return phone.isdigit() and len(phone) == 10

# def clear_form():
#     """Safely clears session state to reset all widgets."""
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]

# --- Main App ---

def disease_detection_from_mri():
    try:
        with open('./models/diabetes_model.sav', 'rb') as f:
            Diabetes_Model = pickle.load(f)
    except Exception:
        Diabetes_Model = None

    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System',
                            ['Brain Tumor', 'Alzemeir Disease', 'Diabetes Detection', 'Pneumonia Detection'],
                            icons=['activity', 'lungs', 'hospital', 'bandaid'],
                            default_index=0)

    if selected in ['Brain Tumor', 'Alzemeir Disease', 'Pneumonia Detection']:
        st.title(f'{selected} Detection')
        
        # Inputs with unique keys
        Patient_Name = st.text_input('Patient Name', key='name')
        
        Phone_number = st.text_input('Mobile Number', key='phone')
        if Phone_number and not validate_mobile(Phone_number):
            st.error("⚠️ Mobile number must be 10 digits.")
        
        Email = st.text_input('Email', key='email')
        if Email and not validate_email(Email):
            st.error("⚠️ Invalid email format.")
            
        Age = st.text_input('Age', key='age')
        upload_file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'], key='file_up')
        
        col1, col2 = st.columns([1, 4])
        
        if col1.button('Predict'):
            if not validate_email(Email) or not validate_mobile(Phone_number):
                st.warning("Please fix the errors above.")
            elif upload_file is None:
                st.info("Please upload an image.")
            else:
                # 1. Save and Predict
                media_folder = "media"
                os.makedirs(media_folder, exist_ok=True)
                file_path = os.path.join(media_folder, upload_file.name)
                with open(file_path, 'wb') as f:
                    f.write(upload_file.getbuffer())
                
                diag = ""
                if selected == 'Brain Tumor':
                    diag = "Brain Tumor Detected" if getResult(file_path) == 1 else "No Brain Tumor"
                elif selected == 'Alzemeir Disease':
                    diag = "Alzheimer's Detected" if alzeimerckh(file_path) == 1 else "No Alzheimer's"
                elif selected == 'Pneumonia Detection':
                    diag = predict_image(file_path)

                st.markdown(f"""
                    <div style="
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #1e3d2f;
                        color: #ffffff;
                        border-radius: 8px;
                        font-size: 20px;
                        font-weight: bold;
                        margin-top: 20px;
                        border: 1px solid #2e7d32;
                        width: 100%;
                    ">
                        Result: {diag}
                    </div>
                """, unsafe_allow_html=True)

                # 2. Email with Robust Toast Trigger
                try:
                    full_content = f"Patient: {Patient_Name}\nResult: {diag}"
                    # Ensure send_email returns True on success
                    status = send_email(full_content, Email, file_path)
                    
                    if status:
                        st.toast("📧 Report sent successfully!", icon="✅")
                    else:
                        st.toast("❌ Email failed to send. Check SMTP settings.", icon="⚠️")
                except Exception as e:
                    st.toast(f"❌ Connection Error: {str(e)}", icon="🚨")

        # Clear button uses on_click to avoid API Exceptions
        # col2.button('Clear Fields', on_click=clear_form)

    # --- Diabetes Section ---
    if selected == 'Diabetes Detection':
        st.title('Diabetes Detection')
        
        D_Name = st.text_input('Patient Name', key='d_name')
        D_Email = st.text_input('Email', key='d_email')
        if D_Email and not validate_email(D_Email):
            st.error("Invalid email.")
            
        D_Age = st.text_input('Age', key='d_age')
        
        c1, c2 = st.columns(2)
        # Using keys for all numeric inputs
        preg = c1.text_input('Pregnancies', key='preg')
        gluc = c2.text_input('Glucose', key='gluc')
        bp = c1.text_input('Blood Pressure', key='bp')
        stk = c2.text_input('Skin Thickness', key='stk')
        ins = c1.text_input('Insulin', key='ins')
        bmi = c2.text_input('BMI', key='bmi')
        dpf = st.text_input('Pedigree Function', key='dpf')

        b1, b2 = st.columns([1, 4])
        
        if b1.button('Test Result'):
            if validate_email(D_Email):
                try:
                    # Convert inputs to float
                    features = [float(x) for x in [preg, gluc, bp, stk, ins, bmi, dpf, D_Age]]
                    res = Diabetes_Model.predict([features])
                    msg = "Diabetic" if res[0] == 1 else "Not Diabetic"
                    st.markdown(f"""
                        <div style="
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #1e3d2f;
                            color: #ffffff;
                            border-radius: 8px;
                            font-size: 20px;
                            font-weight: bold;
                            margin-top: 20px;
                            width: 100%;
                        ">
                            Result: {msg}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Email Logic
                    if sends_email(f"Name: {D_Name}\nResult: {msg}", D_Email):
                        st.toast("📧 Email Sent", icon="✅")
                    else:
                        st.toast("⚠️ Email Failed", icon="❌")
                except ValueError:
                    st.error("Please enter numeric values.")
            else:
                st.error("Enter a valid email.")

        # b2.button('Clear All', on_click=clear_form)

if __name__ == "__main__":
    disease_detection_from_mri()