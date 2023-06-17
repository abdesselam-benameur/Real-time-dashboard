import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import altair as alt
import plotly.graph_objects as go
from dbManager import MongodbCollectionManager
from pymongo import MongoClient
from historical_data import marineHistory

st.set_page_config(page_title="Marine-Weather Dashbord", page_icon="🌊")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">Marine Weather Dashbord</h1>',
            unsafe_allow_html=True)

mongo_client = MongoClient()
collection_manager = MongodbCollectionManager(mongo_client, "Temp_db", "openMeteoMarine")
m_data = collection_manager.get_last_added_item()
now_hour = dt.datetime.now().hour
hourly = m_data["hourly"]
wave_height = hourly["wave_height"][now_hour]
wave_period = hourly["wave_period"][now_hour]
wave_direction = hourly["wave_direction"][now_hour]

delta_height, delta_period, delta_direction = None, None, None
if now_hour != 0:
    delta_height = round(wave_height - hourly["wave_height"][now_hour - 1], 2)
    delta_period = round(wave_period - hourly["wave_period"][now_hour - 1], 2)
    delta_direction = round(wave_direction - hourly["wave_direction"][now_hour - 1], 2)

fig = go.Figure(data=
    go.Scatterpolar(
        r = [0,0.5],
        theta = [0,wave_direction],
        mode = 'lines + markers',
    ))
fig.update_traces(line_width=5, selector=dict(type='scatterpolar'))
fig.update_layout(
    title = " Wave direction",
    title_font_size=10,
    showlegend=False)

#devide into two columns

col1, col2 = st.columns(2)
with col2:
    st.plotly_chart(fig, use_container_width=True)
with col1:
    st.write('  ')
    st.write('  ')
    st.write(' **Wave metrics**')

#adding the metrics in the first column

col1.metric("Wave height ↕️", value=f"{wave_height}m", delta=f"{delta_height}m")
col1.metric("Wave period ⌛", value=f"{wave_period}s", delta=f"{delta_period}s")
col1.metric("Wave direction 🔀", value=f"{wave_direction}°", delta=f"{delta_direction}°")

st.subheader('Wave height and period observed during the time')
labels = ["Wave height (m)", "Wave period (s)"]

@st.cache
def get_data(start_date, end_date):
    m_data = marineHistory(start_date, end_date)
    if m_data is None:
        return None
    hourly = m_data["hourly"]
    wave_height = hourly["wave_height"]
    wave_period = hourly["wave_period"]
    values = [wave_height, wave_period]
    
    date = pd.date_range(start=hourly["time"][0], end=hourly["time"][-1], freq="H")
    df = pd.DataFrame(dict(zip(labels, values)), index=date)

    return df

# date input
col1, col2 = st.columns(2)
start_date = col1.date_input("Start date")
end_date = col2.date_input("End date")

parameters = st.multiselect("Select parameters", labels, "Wave height (m)")

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

mongo_client.close()
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)