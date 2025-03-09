import streamlit as st
from calculations import calculate_lump_sum_payment, calculate_pension

st.title("Federal Benefits Calculator")

# Tabs for different benefit calculations
tab1, tab2 = st.tabs(["Annual Leave Lump Sum", "Pension Estimator"])

with tab1:
    st.header("Annual Leave Lump Sum Calculator")
    name = st.text_input("Employee Name", key="leave_name")
    hourly_rate = st.number_input("Hourly Pay Rate ($)", min_value=0.0, step=0.01, key="hourly_rate")
    leave_balance = st.number_input("Unused Annual Leave Balance (days)", min_value=0.0, step=0.1, key="leave_balance")
    
    if hourly_rate > 0 and leave_balance > 0:
        lump_sum_payment = calculate_lump_sum_payment(hourly_rate, leave_balance)
        st.subheader("Lump Sum Payment Calculation")
        st.write(f"**{name}'s Estimated Lump Sum Payment:** ${lump_sum_payment:,.2f}")

with tab2:
    st.header("Pension Estimator")
    high_3_salary = st.number_input("High-3 Average Salary ($)", min_value=0.0, step=1000.0, key="high_3_salary")
    years_of_service = st.number_input("Years of Federal Service", min_value=0.0, step=0.1, key="years_of_service")
    
    if high_3_salary > 0 and years_of_service > 0:
        pension = calculate_pension(high_3_salary, years_of_service)
        st.subheader("Pension Calculation")
        st.write(f"**Estimated Annual Pension:** ${pension:,.2f}")
