import streamlit as st
from dbManager import MongodbCollectionManager
from pymongo import MongoClient
import datetime
import pandas as pd
from historical_data import weatherHistory

st.set_page_config(page_title="Weather Dashbord", page_icon="⛅")

st.markdown('<h1 style="text-align: center;">Weather Dashbord</h1>',
            unsafe_allow_html=True)

mongo_client = MongoClient("mongodb://localhost:27017/")
collection_manager = MongodbCollectionManager(mongo_client, "Temp_db", "openMeteoWeather")
now_hour = datetime.datetime.now().hour

weather_data = collection_manager.get_last_added_item()
hourly = weather_data["hourly"]
hourly_units = weather_data["hourly_units"]
mongo_client.close()

labels = ["Temperature (°C)", "Apparent Temperature ()", "Precipitation (mm)", "Wind Speed (m/s)", "Humidity (%)"]

temp = hourly["temperature_2m"][now_hour]
temp_unit = hourly_units["temperature_2m"]
precipitation = hourly["precipitation"][now_hour]
precipitation_unit = hourly_units["precipitation"]
wind = hourly["windspeed_10m"][now_hour]
wind_unit = hourly_units["windspeed_10m"]
humidity = hourly["relativehumidity_2m"][now_hour]
humidity_unit = hourly_units["relativehumidity_2m"]

delta_temp, delta_precipitation, delta_wind, delta_humidity = None, None, None, None
if now_hour != 0:
    delta_temp = round(temp - hourly["temperature_2m"][now_hour - 1], 2)
    delta_precipitation = round(precipitation - hourly["precipitation"][now_hour - 1], 2)
    delta_wind = round(wind - hourly["windspeed_10m"][now_hour - 1], 2)
    delta_humidity = round(humidity - hourly["relativehumidity_2m"][now_hour - 1], 2)

col1, col2 = st.columns(2)

col1.metric("Temperature 🌡️", value = f"{temp} {temp_unit}", delta = f"{delta_temp} {temp_unit}")
st.write('Real feel 9°C')
col2.metric("Precipitation 🌧️", value = f"{precipitation} {precipitation_unit}", delta = f"{delta_precipitation} {precipitation_unit}")

col1, col2 = st.columns(2)
col1.metric("Wind Speed 💨", value = f"{wind} {wind_unit}", delta = f"{delta_wind} {wind_unit}")
col2.metric("Humidity 💧", value = f"{humidity} {humidity_unit}", delta = f"{delta_humidity} {humidity_unit}")

@st.cache
def get_data(start_date, end_date):
    # Get the data
    data = weatherHistory(start_date, end_date)
    if data is None:
        return None
    hourly = data["hourly"]

    temp = hourly["temperature_2m"]
    apparent_temp = hourly["apparent_temperature"]
    precipitation = hourly["precipitation"]
    wind = hourly["windspeed_10m"]
    humidity = hourly["relativehumidity_2m"]
    values = [temp, apparent_temp, precipitation, wind, humidity]

    date = pd.date_range(start=hourly["time"][0], end=hourly["time"][-1], freq="H")
    df = pd.DataFrame(dict(zip(labels, values)), index=date)
    return df

# date input
col1, col2 = st.columns(2)
start_date = col1.date_input("Start date")
end_date = col2.date_input("End date")

parameters = st.multiselect("Select parameters", labels, "Temperature (°C)")
if parameters:
    # Get the data
    df = get_data(start_date, end_date)
    if df is not None:
        # Plot the data
        st.line_chart(df.loc[:, parameters], use_container_width=True, height=400, width=0)
    else:
        st.warning("No data available for the selected dates")
else:
    st.warning("Please select parameters to plot")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)