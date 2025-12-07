import streamlit as st
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in first!")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import datetime as dt

# Fetching the api key 
load_dotenv()
Weather_Api_key=os.getenv("Weather_Api_key") 

def get_weather_forecast(city_name, date):
    try:
        today = dt.datetime.now().date()
        # Ensure the date string is in the correct format for conversion
        forecast_date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        max_date = today + dt.timedelta(days=15)
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}, 400

    if forecast_date < today:
        return {"error": "Cannot request weather for a past date."}, 400
        
    elif forecast_date > max_date:
        return {"error": f"Forecast date cannot be more than 15 days away from today ({today})."}, 400

    URL = "http://api.weatherapi.com/v1/forecast.json" 
    params = {
        "q": city_name, 
        "key": Weather_Api_key,
        "dt": date
    }
    
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status() 
        data = response.json()
        
        if "forecast" in data and "forecastday" in data["forecast"]:
            day_data = data["forecast"]["forecastday"][0]["day"]
            weather_info = {
                "date": date, 
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "maximum_temperature_c": day_data["maxtemp_c"],
                "minimum_temperature_c": day_data["mintemp_c"],
                "condition": day_data["condition"]["text"]
            }
            return weather_info
        else:
            return {"error": "Weather data structure not found in API response."}
            
    except requests.exceptions.HTTPError as e:
        return {"error": f"External API error: {e}"}
    except requests.exceptions.RequestException:
        return {"error": "Could not connect to the external weather service."}
        
st.markdown("""
<style>

.stApp {
    background-color:#edf6fc ; 
    color: #333333; 
    font-family: 'Open Sans', sans-serif; 
}
.banner-container {
        background-color:#92cae2; 
        height: 300px;
        display: flex;
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        color: white; 
        padding: 20px;
        margin-bottom: 50px;
    }

.banner-container h1 {
        font-family: 'Ostwald'; 
        font-size: 3.8rem; 
        font-weight: bold;
        color: #FFFFFF    ;
        text-align: center;
    }
.banner-container h2 {
        font-family: 'Ostwald'; 
        font-size: 1.5rem; 
        font-weight: bold;
        color: #FFFFFF    ;
        text-align: center;
        }

.stForm {
    position: relative;
    z-index: 10; 
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 50px; 
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.stTextInput label, .stDateInput label {
    background-color: #ffffff;
    color:#333333;
    font-weight: bold;
}

.stButton>button {
    background-color: #ffffff;
    color: #333333;
    border-radius: 50px; 
    border: none;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
    transition: all 0.2s;
    height: 100%; 
    margin-top: 29px; 
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #5aa4c1;
    transform: translateY(-1px);
}

.stSuccess > div, .stError > div, .stWarning > div {
    background-color: #ffffff; 
    color: #ffffff;
    border-left: 5px solid #92cae2;
    border-radius: 5px;
}

.st-emotion-cache-1pxx76e, .st-emotion-cache-1c9fex {
    background-color: #ffffff;
    color: #333333;
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.05);
    text-align: center;
}

.st-emotion-cache-1wivd6d p {
    background-color: #ffffff;
    color: #333333;
}
.st-emotion-cache-1wivd6d .css-1qxtsqg {
    background-color: #ffffff;
    color: #333333;
    font-size: 2em;
    font-weight: 600;
}
.result-container {
        background-color:#92cae2; 
        height: 300px;
        display: flex;
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        color: white; 
        padding: 20px;
        border-radius: 40px;
        margin-bottom: 50px;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15)
    }
.result-container h1 {
        font-family: 'Ostwald'; 
        font-size: 3.8rem; 
        font-weight: bold;
        color: #FFFFFF    ;
        text-align: center;
    }
.result-container h2 {
        font-family: 'Ostwald'; 
        font-size: 2rem; 
        font-weight: bold;
        color: #FFFFFF    ;
        text-align: center;
        }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="banner-container">
        <h1>Weather Information</h1>
        <h2>Plan your trip with accurate weather forecasts!!</h2>
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Weather Forecast App", layout="wide")

with st.form("weather_form"):
    
    col_city, col_date, col_button = st.columns([4, 3, 1])
    
    with col_city:
        city_input = st.text_input(
            "Enter City Name:", 
            placeholder="Enter city name...",
            label_visibility="visible", 
        )

    with col_date:
        today = datetime.now().date()
        max_forecast_date = today + timedelta(days=15)
        date_input = st.date_input(
           "Select Date:",
           value=today,
           min_value=today,
           max_value=max_forecast_date,
           format="YYYY/MM/DD",
           label_visibility="visible", 
        )

    with col_button:
        submitted = st.form_submit_button("Search 🔍")

if submitted:
    date_str = date_input.strftime("%Y-%m-%d")
    if not city_input:
        st.error("Please enter a city name.")
    else:
        with st.spinner(f'Fetching forecast for *{city_input}* on *{date_str}*...'):
            forecast_data = get_weather_forecast(city_input, date_str)
        
        st.markdown("---")

        if "error" in forecast_data:
            # Display error from the backend (e.g., invalid date range)
            st.error(f"Weather Fetch Failed: {forecast_data['error']}")
        elif forecast_data:
            st.success("Forecast Retrieved Successfully! 🥳")
            
            st.markdown(
                f'<div class="result-container">'
                f'<h1>{forecast_data["city"]}</h1>'
                f'<h2> Date: {forecast_data["date"]}</h2>' 
                f'<h2> 🌥️ {forecast_data["condition"]}</h2>'
                f'<h2> Minimum Temperature: {forecast_data["minimum_temperature_c"]}°C | Maximum Temperature: {forecast_data["maximum_temperature_c"]}°C </h2>'
                f'</div>',
                unsafe_allow_html=True
            )

        else:
            
            st.warning("Could not retrieve weather data. Please check the city name.")

col_btn1, col_large_gap,col_btn2,col_large_gap,col_btn3 = st.columns([12, 50,10,50, 11])

with col_btn1:
    if st.button("<--Back"):
        st.switch_page("pages/02_Tourist_Spots.py")
with col_btn2:
    if st.button("Home"):
        st.switch_page("pages/01_Home_Page.py")
with col_btn3:
    if st.button("Next-->"):
        st.switch_page("pages/04_Currency_Converter.py")