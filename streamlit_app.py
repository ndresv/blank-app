import streamlit as st
import requests
from streamlit_folium import folium_static
import folium


api_key="8f1eeedc-4607-4093-b68c-9dcf1785a002"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

@st.cache_data
def map_creator(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)
    folium_static(m)

@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict

category = st.selectbox("Select Input Method", ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"])

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = [i["country"] for i in countries_dict["data"]]
        country_selected = st.selectbox("Select a country", options=countries_list)
        
        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = [i["state"] for i in states_dict["data"]]
                state_selected = st.selectbox("Select a state", options=states_list)
                
                if state_selected:
                    cities_dict = generate_list_of_cities(state_selected, country_selected)
                    if cities_dict["status"] == "success":
                        cities_list = [i["city"] for i in cities_dict["data"]]
                        city_selected = st.selectbox("Select a city", options=cities_list)
                        
                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()
                            
                            st.write(aqi_data_dict)  # Debugging line to print the API response
                            
                            if aqi_data_dict["status"] == "success":
                                data = aqi_data_dict["data"]
                                st.write(f"Temperature: {data['current']['weather']['tp']} °C")
                                st.write(f"Humidity: {data['current']['weather']['hu']} %")
                                st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
                                map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])
                            else:
                                st.warning("No data available for this location.")

elif category == "By Nearest City (IP Address)":
    if st.button("Get Data by IP Address"):
        url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
        aqi_data_dict = requests.get(url).json()
        
        st.write(aqi_data_dict)  # Debugging line to print the API response
        
        if aqi_data_dict["status"] == "success":
            data = aqi_data_dict["data"]
            st.write(f"Temperature: {data['current']['weather']['tp']} °C")
            st.write(f"Humidity: {data['current']['weather']['hu']} %")
            st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
            map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])
        else:
            st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter Latitude")
    longitude = st.text_input("Enter Longitude")
    
    if latitude and longitude:
        if st.button("Get Data by Coordinates"):
            url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
            aqi_data_dict = requests.get(url).json()
            
            st.write(aqi_data_dict)  # Debugging line to print the API response
            
            if aqi_data_dict["status"] == "success":
                data = aqi_data_dict["data"]
                st.write(f"Temperature: {data['current']['weather']['tp']} °C")
                st.write(f"Humidity: {data['current']['weather']['hu']} %")
                st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
                map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])
            else:
                st.warning("No data available for this location.")
