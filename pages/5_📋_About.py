import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="About", page_icon="📋")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("About Us")
st.write("This project is part of ***Systems for Data Science*** program of the Master ***MLSD***")
st.write("``Machine Learning for Data Science``")
st.write("Realized by:")
st.write(" - Abdesselam BENAMEUR")
st.write(" - Hakim IGUENI")
st.write(" - Doha EL HITARY")
st.write(" - Anis HAOUA")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)