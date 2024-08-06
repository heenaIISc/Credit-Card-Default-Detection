# streamlit_app.py

import streamlit as st
import pandas as pd

from src.CreditCardDefaultsPrediction.pipelines.prediction_pipeline import PredictPipeline
from src.CreditCardDefaultsPrediction.utils.utils import Utils
from src.CreditCardDefaultsPrediction.utils.data_processor import DBProcessor

# Ingest data from MongoDB
data = Utils().run_data_pipeline(DBProcessor(), "mongodb+srv://root:root@cluster0.k3s4vuf.mongodb.net/?retryWrites=true&w=majority&ssl=true", "credit_card_defaults/data")

# Drop dolumns
data.drop(['DEFAULT_PAYMENT', "_id", "ID"], axis=1, inplace=True)

# Design Streamlit Page
st.write("""
# Credit Card Default Detection
This app predicts the **Credit Card Payment Defaults**!
""")
st.write('---')

# Sidebar
# Header of Specify Input Parameters
st.sidebar.header('Specify Input Parameters')


def user_input_features(data):
    limit_balance = st.number_input("LIMIT BALANCE:")

    # Dropdown to select text option for SEX
    sex_dict = {'Male': 1, 
                'Female': 2}
    sex = st.sidebar.selectbox('SEX:', list(sex_dict.keys()))

    # Dropdown to select text option for EDUCATION
    education_dict = {'Graduate School': 1, 
                      'University': 2, 
                      'High School': 3, 
                      'Others': 4}
    education = st.sidebar.selectbox('EDUCATION:', list(education_dict.keys()))

    # Dropdown to select text option for MARRIAGE
    marriage_dict = {'Married': 1, 
                     'Single': 2,
                     'Others': 3}
    marriage = st.sidebar.selectbox('MARRIAGE:', list(marriage_dict.keys()))

    age = st.sidebar.slider('AGE', int(data['AGE'].min()), int(data['AGE'].max()), int(data['AGE'].mean()))

    # Dropdown to select text option for PAY SEPT
    pay_sept_dict = {'No Consumption': -2, 
                     'Pay Duly': -1, 
                     'Revolving': 0,  
                     'Delayed for 1 month': 1, 
                     'Delayed for 2 months': 2, 
                     'Delayed for 3 months': 3, 
                     'Delayed for 4 months': 4, 
                     'Delayed for 5 months': 5, 
                     'Delayed for 6 months': 6, 
                     'Delayed for 7 months': 7, 
                     'Delayed for 8 months': 8, 
                     'Delayed for 9 months and above': 9}
    pay_sept = st.sidebar.selectbox('PAY SEPTEMBER:', list(pay_sept_dict.keys()))

    # Dropdown to select text option for PAY AUG
    pay_aug_dict = {'No Consumption': -2, 
                    'Pay Duly': -1, 
                    'Revolving': 0,  
                    'Delayed for 1 month': 1, 
                    'Delayed for 2 months': 2, 
                    'Delayed for 3 months': 3, 
                    'Delayed for 4 months': 4, 
                    'Delayed for 5 months': 5, 
                    'Delayed for 6 months': 6, 
                    'Delayed for 7 months': 7, 
                    'Delayed for 8 months': 8, 
                    'Delayed for 9 months and above': 9}
    pay_aug = st.sidebar.selectbox('PAY AUGUST:', list(pay_aug_dict.keys()))

    # Dropdown to select text option for PAY JUL
    pay_jul_dict = {'No Consumption': -2,
                    'Pay Duly': -1, 
                    'Revolving': 0,  
                    'Delayed for 1 month': 1, 
                    'Delayed for 2 months': 2, 
                    'Delayed for 3 months': 3, 
                    'Delayed for 4 months': 4, 
                    'Delayed for 5 months': 5, 
                    'Delayed for 6 months': 6, 
                    'Delayed for 7 months': 7, 
                    'Delayed for 8 months': 8, 
                    'Delayed for 9 months and above': 9}
    pay_jul = st.sidebar.selectbox('PAY JULY:', list(pay_jul_dict.keys()))

    # Dropdown to select text option for PAY JUN
    pay_jun_dict = {'No Consumption': -2, 
                    'Pay Duly': -1, 
                    'Revolving': 0,  
                    'Delayed for 1 month': 1, 
                    'Delayed for 2 months': 2, 
                    'Delayed for 3 months': 3, 
                    'Delayed for 4 months': 4, 
                    'Delayed for 5 months': 5, 
                    'Delayed for 6 months': 6, 
                    'Delayed for 7 months': 7, 
                    'Delayed for 8 months': 8, 
                    'Delayed for 9 months and above': 9}
    pay_jun = st.sidebar.selectbox('PAY JUNE:', list(pay_jun_dict.keys()))

    # Dropdown to select text option for PAY MAY
    pay_may_dict = {'No Consumption': -2, 
                    'Pay Duly': -1, 
                    'Revolving': 0,  
                    'Delayed for 1 month': 1, 
                    'Delayed for 2 months': 2, 
                    'Delayed for 3 months': 3, 
                    'Delayed for 4 months': 4, 
                    'Delayed for 5 months': 5, 
                    'Delayed for 6 months': 6, 
                    'Delayed for 7 months': 7, 
                    'Delayed for 8 months': 8, 
                    'Delayed for 9 months and above': 9}
    pay_may = st.sidebar.selectbox('PAY MAY:', list(pay_may_dict.keys()))

    # Dropdown to select text option for PAY APR
    pay_apr_dict = {'No Consumption': -2, 
                    'Pay Duly': -1, 
                    'Revolving': 0,  
                    'Delayed for 1 month': 1, 
                    'Delayed for 2 months': 2, 
                    'Delayed for 3 months': 3, 
                    'Delayed for 4 months': 4, 
                    'Delayed for 5 months': 5, 
                    'Delayed for 6 months': 6, 
                    'Delayed for 7 months': 7, 
                    'Delayed for 8 months': 8, 
                    'Delayed for 9 months and above': 9}
    pay_apr = st.sidebar.selectbox('PAY APRIL:', list(pay_apr_dict.keys()))

    # TextField to enter Bill AMOUNTS

    # Create six columns
    bill_columns = st.columns(6)

    # Add a textfield to each column
    bill_amount_sept, bill_amount_aug, bill_amount_jul, bill_amount_jun, bill_amount_may, bill_amount_apr = bill_columns

    bill_amount_sept = bill_amount_sept.number_input("BILL AMOUNT SEPTEMBER:")
    bill_amount_aug = bill_amount_aug.number_input("BILL AMOUNT AUGUST:")
    bill_amount_jul = bill_amount_jul.number_input("BILL AMOUNT JULY:")
    bill_amount_jun = bill_amount_jun.number_input("BILL AMOUNT JUNE:")
    bill_amount_may = bill_amount_may.number_input("BILL AMOUNT MAY:")
    bill_amount_apr = bill_amount_apr.number_input("BILL AMOUNT APRIL:")

    # TextField to enter PAID AMOUNTS

     # Create six columns
    pay_columns = st.columns(6)

     # Add a textfield to each column
    pay_amount_sept, pay_amount_aug, pay_amount_jul, pay_amount_jun, pay_amount_may, pay_amount_apr = pay_columns
    
    pay_amount_sept = pay_amount_sept.number_input("PAY AMOUNT SEPTEMBER:")
    pay_amount_aug = pay_amount_aug.number_input("PAY AMOUNT AUGUST:")
    pay_amount_jul = pay_amount_jul.number_input("PAY AMOUNT JULY:")
    pay_amount_jun = pay_amount_jun.number_input("PAY AMOUNT JUNE:")
    pay_amount_may = pay_amount_may.number_input("PAY AMOUNT MAY:")
    pay_amount_apr = pay_amount_apr.number_input("PAY AMOUNT APRIL:")

    data = {
                'LIMIT_BAL': float(limit_balance),
                'SEX': sex_dict[sex] if sex in sex_dict else 0,
                'EDUCATION': education_dict[education] if education in education_dict else 0,
                'MARRIAGE': marriage_dict[marriage] if marriage in marriage_dict else 0,
                'AGE': int(age), 
                'PAY_SEPT': pay_sept_dict[pay_sept] if pay_sept in pay_sept_dict else 0,
                'PAY_AUG': pay_aug_dict[pay_aug] if pay_aug in pay_aug_dict else 0,
                'PAY_JUL': pay_jul_dict[pay_jul] if pay_jul in pay_jul_dict else 0,
                'PAY_JUN': pay_jun_dict[pay_jun] if pay_jun in pay_jun_dict else 0,
                'PAY_MAY': pay_may_dict[pay_may] if pay_may in pay_may_dict else 0,
                'PAY_APR': pay_apr_dict[pay_apr] if pay_apr in pay_apr_dict else 0,
                'BILL_AMT_SEPT': float(bill_amount_sept),
                'BILL_AMT_AUG': float(bill_amount_aug),
                'BILL_AMT_JUL': float(bill_amount_jul),
                'BILL_AMT_JUN': float(bill_amount_jun),
                'BILL_AMT_MAY': float(bill_amount_may),
                'BILL_AMT_APR': float(bill_amount_apr),
                'PAY_AMT_SEPT': float(pay_amount_sept),
                'PAY_AMT_AUG': float(pay_amount_aug),
                'PAY_AMT_JUL': float(pay_amount_jul),
                'PAY_AMT_JUN': float(pay_amount_jun),
                'PAY_AMT_MAY': float(pay_amount_may),
                'PAY_AMT_APR': float(pay_amount_apr)
            }
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features(data)

# Main Panel
# Print specified input parameters
st.header('Specified Input parameters')
st.write(df)
st.write('---')

predict_pipeline = PredictPipeline()
prediction = predict_pipeline.predict(df)

st.header('Customer will')
st.write("DEFAULT" if prediction[0] == 1 else "NOT DEFAULT")

st.write('---')
