import streamlit as st
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in first!")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.title("Currency Converter")
st.write("Convert currencies instantly!!")

st.markdown("""
<style>

.stApp {
    background-color:#edf6fc ; 
    color: #333333; 
    font-family: 'Open Sans', sans-serif; 
}
</style>

    """, unsafe_allow_html=True)
rates={
    "USD":1,
    "INR":83.10,
    "EUR":0.92,
    "GBP":0.78,
    "JPY":148.50,
    "AUD":1.52,
    "CAD":1.36,
    "SGD":1.34,
    "AED":3.67
}

col1,col2=st.columns(2)

with col1:
    from_currency=st.selectbox("From Currency",rates.keys())

with col2:
    to_currency=st.selectbox("To Currency",rates.keys())

amount=st.number_input("Enter Amount",min_value=0.0,value=1.0)

if st.button("Convert"):
    usd_amount=amount/rates[from_currency]
    final_amount=usd_amount*rates[to_currency]
    st.success(f"{amount}{from_currency}={final_amount:.2f}{to_currency}")

col_btn1, col_large_gap,col_btn2,col_large_gap,col_btn3 = st.columns([12, 50,10,50, 11])

with col_btn1:
    if st.button("<--Back"):
        st.switch_page("pages/03_weather_info.py")
with col_btn2:
    if st.button("Home"):
        st.switch_page("pages/01_home_page.py")
with col_btn3:
    if st.button("Next-->"):
        st.switch_page("pages/02_tourist_spots.py")