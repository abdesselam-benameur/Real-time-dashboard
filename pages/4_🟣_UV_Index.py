import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pymongo import MongoClient
from dbManager import MongodbCollectionManager
from historical_data import uvHistory

st.set_page_config(page_title="UV Index Dashbord", page_icon="🟣")

# # ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">UV Dashbord</h1>',
            unsafe_allow_html=True)


mongo_client = MongoClient()
collection_manager = MongodbCollectionManager(mongo_client, "Temp_db", "openUV")

uv_data = collection_manager.get_last_added_item()["result"]
uv_index = uv_data["uv"]
uv_max = uv_data["uv_max"]
uv_max_time = uv_data["uv_max_time"][:-5].replace("T", " ")
sun_times = uv_data["sun_info"]["sun_times"]
sunrise = sun_times["sunrise"][:-5].replace("T", " ")
sunset = sun_times["sunset"][:-5].replace("T", " ")

mongo_client.close()

def get_uv_index_color_and_text():
    if uv_index < 3:
        return 'green', 'Low'
    elif uv_index < 6:
        return 'yellow', 'Moderate'
    elif uv_index < 8:
        return 'orange', 'High'
    elif uv_index < 11:
        return 'red', 'Very High'
    else:
        return 'violet', 'Extreme'


def get_last_update():
    return dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_data(start_date, end_date):
    uv_data = uvHistory(start_date, end_date)
    if uv_data is None:
        return None
    hourly = uv_data["hourly"]
    date = pd.date_range(start=hourly["time"][0], end=hourly["time"][-1], freq="H")
    return pd.DataFrame({"UV index": hourly["uv_index"]}, index=date)


container = st.container()
col1, col2, col3, col4 = container.columns(4)
with col1:
    color, text = get_uv_index_color_and_text()
    st.metric("🟣 UV Index:", uv_index)
    st.markdown('<strong style="color: {}; font-size: 1.6em">{}</strong>'.format(color, text),
                unsafe_allow_html=True)
with col2:
    st.write('⬆️ Max UV Index: ``{}``'.format(uv_max),
             unsafe_allow_html=True)
    st.write("</br>", unsafe_allow_html=True)
    st.write(' 🕛 Max UV Index time: ``{}``'.format(uv_max_time),
             unsafe_allow_html=True)

with col3:
    st.write(' 🌅 Surnise:</br>``{}``'.format(sunrise),    unsafe_allow_html=True)
    st.write("</br>", unsafe_allow_html=True)
    st.write(' 🌇 Sunset:</br>``{}``'.format(sunset),    unsafe_allow_html=True)
with col4:
    st.write(" 📥 Last update: ``{}``".format(get_last_update()))
    st.write("</br>", unsafe_allow_html=True)
    st.write(' 📊 Data source: [OpenUV](https://www.openuv.io/)')


with st.expander("More info 🔽"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<table> <tr> <th>UV Index</th> <th>Level</th> </tr> <tr> <td style="color: green;">0-2</td> <td style="color: green;">Low</td> </tr> <tr> <td style="color: yellow;">3-5</td> <td style="color: yellow;">Moderate</td> </tr> <tr> <td style="color: orange;">6-7</td> <td style="color: orange;">High</td> </tr> <tr> <td style="color: red;">8-10</td> <td style="color: red;">Very High</td> </tr> <tr> <td style="color: violet;">11+</td> <td style="color: violet;">Extreme</td> </tr> </table>""", unsafe_allow_html=True)
    with col2:
        st.write("UV Index is a measure of the strength of the sun's ultraviolet rays at a particular place and time. The higher the UV Index value, the greater the need for eye and skin protection. The UV Index is forecast as a number from 0 to 11+.")

# date input
col1, col2 = st.columns(2)
start_date = col1.date_input("Start date")
end_date = col2.date_input("End date")
# Get the data
df = get_data(start_date, end_date)
if df is not None:
    # Plot the data
    st.line_chart(df, use_container_width=True, height=400, width=0)
else:
    st.warning("No data available for the selected dates")
    

st.write(' 📊 Graph source: [OpenMeteo](https://open-meteo.com/en/docs/air-quality-api#latitude=40.71&longitude=-74.01&hourly=uv_index)')
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)