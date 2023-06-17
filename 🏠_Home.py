import streamlit as st
import pandas as pd
import numpy as np


# emojies: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Nice City Dashbord",
                   page_icon="🇫🇷",
                   layout="wide")
# st.set_theme("light")
# ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'> 🇫🇷 Nice  City Weather Dashbord</h1>",
            unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'></h1>",
            unsafe_allow_html=True)
st.markdown("""<p style='font-size:1.4em'>Welcome to our real-time data visualization dashboard for tracking weather changes in the city of Nice 🇫🇷.</br>
</br>
This dashboard has been developed to provide real-time information on current and future weather conditions, as well as air quality and marine conditions.</br>
</br>
It allows for visualizing, analyzing and understanding weather phenomena to make informed decisions.</br>
</br>
The data used to feed this dashboard was retrieved from various reliable sources such as weather data, marine data, and air quality data.</br>
</br>
Don't hesitate to explore the different sections of this dashboard to learn more about the weather conditions in your city.</br>
</br>
We hope this tool will be useful for you!</p>""", unsafe_allow_html=True)

# add a line to separate the title from the rest of the page
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)