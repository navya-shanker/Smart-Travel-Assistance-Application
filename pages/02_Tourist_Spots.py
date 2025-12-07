import streamlit as st
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in first!")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

import requests
import pandas as pd 
import os
from dotenv import load_dotenv
#Fetching the api key 
from dotenv import load_dotenv
load_dotenv()
Map_api_key=os.getenv("Map_api_key")
if not Map_api_key:
    Map_api_key=st.secrets["Map_api_key"]
    
radius=25000 #25km radius of the city
if 'city_data' not in st.session_state:
    st.session_state.city_data = None
    
def get_city_coordinates(city,Map_api_key):
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city, 
        "apiKey": Map_api_key,
        "limit": 1}
    response = requests.get(url,params=params)
    if response.status_code == 200:    #all well with url if you get 200
        data = response.json()
        if data.get('features'):
            latitude=(data['features'][0]['properties']['lat'])
            longitude=(data['features'][0]['properties']['lon'])
            return latitude,longitude
        else:
            return None,None
    else:
        return None,None
    
def get_city_attractions(latitude,longitude,Map_api_key,radius):
    attractions = []
    url = "https://api.geoapify.com/v2/places"
    Categories="tourism.attraction"
    params = {
        "categories":Categories,
        "filter": f"circle:{longitude},{latitude},{radius}",
        "apiKey": Map_api_key,
        "limit": 50}
    response=requests.get(url,params=params)
    if response.status_code == 200:    #all well with url if you get 200
        data = response.json()
        if data.get('features'):
            for feature in data['features']:
                attraction=feature['properties']['name']
                if attraction not in attractions and len(attractions)<20:
                    attractions.append(attraction)
    return attractions

def get_city_restaurants(latitude,longitude,Map_api_key,radius):
    url = "https://api.geoapify.com/v2/places"
    Categories="catering.restaurant,catering.cafe"
    params = {
        "categories":Categories,
        "filter": f"circle:{longitude},{latitude},{radius}",
        "apiKey": Map_api_key,
        "limit": 50}
    restaurants=[]
    response=requests.get(url,params=params)
    if response.status_code == 200:    #all well with url if you get 200
        data = response.json()
        if data.get('features'):
            for feature in data['features']:
                restaurant=feature['properties']['name']
                if restaurant not in restaurants and len(restaurants)<20:
                    restaurants.append(restaurant)
    return restaurants

#wrapper function
def get_city_info(city_input):
    
    latitude, longitude = get_city_coordinates(city_input, Map_api_key)
    
    if not latitude or not longitude:
        print(f"Could not find coordinates for {city_input}.")
        return None
    
    attractions = get_city_attractions(latitude, longitude, Map_api_key, radius)
    restaurants = get_city_restaurants(latitude, longitude, Map_api_key, radius)
    
    city_data = {
        'city': city_input,
        'latitude': latitude,
        'longitude': longitude,
        'attractions': attractions,
        'restaurants': restaurants
    }
    
    return city_data

st.set_page_config(page_title="City explorer", layout="wide")

st.markdown("""

<style>

.stApp {
    background-color: #edf6fc; 
    color: #333333;   
    font-family: 'Open Sans', sans-serif      
    }
            
.banner-container {
    background-color: #92cae2; 
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
.stTextInput > div > div { 
    margin-left: auto; 
    margin-right: auto;
}
.stTextInput > div > div > input { 
    background: #ffffff ;
        color:black
    border: none ;
    padding: 14px 18px ;
    border-radius: 50px ;
    width: 100% ;
    font-size: 17px ;
    box-shadow:
        6px 6px 12px rgba(0, 0, 0, 0.15),
        -6px -6px 12px rgba(255, 255, 255, 0.85) !important; 
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
</style>

    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="banner-container">
        <h1>Discover Amazing Places</h1>
        <h2>Explore the best tourist spots and restaurants in the area!!</h2>
    </div>
    """, unsafe_allow_html=True)

col_spacer1, col_input, col_spacer2 = st.columns([1, 4, 1])

with col_input:
    city_input = st.text_input("Search for places...",placeholder="Enter city name...",label_visibility="collapsed")
    search_button = st.button('Search City Explorer 🔍', type="primary")


if search_button and city_input:
    with st.spinner(f'Loading data for {city_input.title()}...'):
        
        results = get_city_info(city_input)
        st.session_state.city_data = results

if st.session_state.city_data:
    data = st.session_state.city_data
    st.markdown("---") 
    
    if 'error' in data:
        st.error(f"Could not retrieve data: {data['error']}")
    else:
        st.header(f"Data for {data['city'].title()}")
        
        if 'latitude' in data and 'longitude' in data:
            lat = data['latitude']
            lon = data['longitude']
            
            st.subheader("Location and Search Area Overview")
            map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
            st.map(map_df, zoom=10) 
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### 📍 Attractions Found ({len(data.get('attractions', []))})")
                if data.get('attractions'):
                    df_attractions=pd.DataFrame({'Attraction Name': data['attractions']})
                    N=len(df_attractions)
                    df_attractions.index = pd.RangeIndex(start=1, stop=N + 1, step=1)
                    st.dataframe(
                        df_attractions,
                        width='stretch'
                    )
                else:
                    st.warning("No attractions found in this area.")
                
            with col2:
                st.markdown(f"### 🍽️ Restaurants/Cafes Found ({len(data.get('restaurants', []))})")
                if data.get('restaurants'):
                    df_restaurants=pd.DataFrame({'Restaurant/Cafe Name': data['restaurants']})
                    N=len(df_restaurants)
                    df_restaurants.index = pd.RangeIndex(start=1, stop=N + 1, step=1)
                    st.dataframe(
                        df_restaurants,
                        width='stretch'
                    )
                else:
                    st.warning("No restaurants or cafes found in this area.")
        else:
             st.error("Received data but latitude/longitude are missing. Please check the `app.py` logic.")

col_btn1, col_large_gap,col_btn2,col_large_gap,col_btn3 = st.columns([12, 50,10,50, 11])

with col_btn1:
    if st.button("<--Back"):
        st.switch_page("pages/04_Currency_Converter.py")
with col_btn2:
    if st.button("Home"):
        st.switch_page("pages/01_Home_Page.py")
with col_btn3:
    if st.button("Next-->"):
        st.switch_page("pages/03_Weather_Info.py")