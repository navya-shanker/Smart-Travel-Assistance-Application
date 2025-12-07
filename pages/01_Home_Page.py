import streamlit as st
import os
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in first!")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.set_page_config(page_title="Travel Assisstant system",layout="wide")
st.title("Welcome to the Smart Travel Assisstance System 🏝️✈️🧳")
st.header("Your one step travel companion!!")


image_path = os.path.join(os.path.dirname(__file__), '..', 'bg.jpg')
st.image(image_path,width="stretch")

col1,col2,col3=st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Top Destinations📍 and Restaraunts🍽️")
        st.write("Discover the best places around the world and authentic dine-in places")
        if st.button(label="Explore",key="btn1"):
            st.switch_page("pages/02_Tourist_Spots.py")
            
with col2:
    with st.container(border=True):    
        st.header("Weather Information🌨️☀️🍃")
        st.write("Check the latest weather forecats for your trips.")
        if st.button(label="Check weather",key="btn2"):
            st.switch_page("pages/03_Weather_Info.py")
            
            
with col3:
    with st.container(border=True):
        st.header("Currency Converter💲💱")
        st.write("Convert currencies for your international trips")
        if st.button(label="Convert currency",key="btn3"):
            st.switch_page("pages/04_Currency_Converter.py")
           
          
          
          
       



