#['inquiry', 'fico', 'revolving_balance', 'intrest_rate', 'days', 'dti',
  #     'annual_income', 'installment', 'revol.util', 'fully_paid']
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('loan_data.csv')

model = pickle.load(open('model.pkl','rb'))


nav = st.sidebar.radio("Navigation",["Home","MEETS POLICY"])
if nav =="Home":
    st.title("GET YOUR LOAN APPROVED")
    st.image('loan.jpg',width=800)
    if st.checkbox("show table"):
        st.table(data.head(10))
    graph = st.selectbox("What kind of graph?",["Interactive","Non interactive"])

    if graph == "Interactive":
        st.success("More than 80% of our customers get their loans approved."
                   "Apply for a loan and get your loan approved today.")
        count = data['credit.policy'].value_counts()
        plt.pie(count, autopct='%0.2f%%', labels=("Approved", "Not Approved"))
        st.pyplot()


    if graph == "Non interactive":
        plt.figure(figsize=(10,6))
        cross = pd.crosstab(data['purpose'],data['credit.policy'])
        cross.plot(kind='bar')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()



if nav =="MEETS POLICY":
    st.title('SEE IF YOU CAN APPROVE LOAN')
    inquiry = st.number_input('Enter inquiry in the last 6 months',step=1)
    fico = st.number_input('Enter credit_score',step=1)
    revolving_balance = st.number_input('Enter revolving_balance',step=1)
    intrest_rate = st.number_input('Enter intrest_rate',step=1)/100
    days = st.number_input('Enter number of days with loan',step=1)
    dti = st.number_input('Enter dti',step=1)
    annual_income = st.number_input('Enter annual_income',step=1)
    installment = st.number_input('Enter installment',step=1)
    utilization_rate = st.number_input('Enter utilization_rate',step=1)
    paid = st.selectbox('Choose if loan is fully paid or not',('yes','no'))
    fully_paid = []
    if paid == 'yes':
        fully_paid = 1
    else:
        fully_paid = 0

    if st.button('Enter'):
        result = model.predict([[inquiry, fico, revolving_balance,intrest_rate, days, dti,
           annual_income, installment, utilization_rate, fully_paid]])
        if result == 1:
            st.success('Loan can be approved')
        elif result ==0:
            st.success('Loan cannot be approved')
        else:
            st.success('fill in')
