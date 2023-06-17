import streamlit as st
import pandas as pd
import datetime as dt
from dbManager import MongodbCollectionManager
from pymongo import MongoClient
from historical_data import airqualityHistory

st.set_page_config(page_title="Air Quality Dashbord", page_icon="🌫️")

# ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">Air Quality Dashbord</h1>',
            unsafe_allow_html=True)
with st.empty():
    st.markdown('<h3 style="text-align: center;">    </br> </br>   </h3>',
                unsafe_allow_html=True)


mongo_client = MongoClient()
collection_manager = MongodbCollectionManager(
    mongo_client, "Temp_db", "airQuality")

aq_data = collection_manager.get_last_added_item()
air_index = aq_data["hourly"]["european_aqi"][dt.datetime.now().hour]
mongo_client.close()

# Labels
labels = ['Particulate Matter PM10 (μg/m³)', 'Particulate Matter PM2.5 (μg/m³)',
          'Carbon Monoxide CO (μg/m³)', 'Nitrogen Dioxide NO2 (μg/m³)',
          'Sulphur Dioxide SO2 (μg/m³)', 'Ozone O3 (μg/m³)', 'European Air Quality Index AQI']


@st.cache
def get_data(start_date, end_date):
    aq_data = airqualityHistory(start_date, end_date)
    if aq_data is None:
        return None
    hourly = aq_data["hourly"]
    # Values
    pm10 = hourly["pm10"]
    pm2_5 = hourly["pm2_5"]
    co = hourly["carbon_monoxide"]
    no2 = hourly["nitrogen_dioxide"]
    so2 = hourly["sulphur_dioxide"]
    o3 = hourly["ozone"]
    aqi = hourly["european_aqi"]
    values = [pm10, pm2_5, co, no2, so2, o3, aqi]

    date = pd.date_range(start=hourly["time"]
                         [0], end=hourly["time"][-1], freq="H")
    df = pd.DataFrame(dict(zip(labels, values)), index=date)

    return df


def get_color_and_description(air_index):
    if 0 <= air_index <= 50:
        return "green", "GOOD"
    elif 51 <= air_index <= 100:
        return "yellow", "MODERATE"
    elif 101 <= air_index <= 150:
        return "orange", "BAD FOR SENSITIVE GROUPS"
    elif 151 <= air_index <= 200:
        return "red", "BAD"
    elif 201 <= air_index <= 300:
        return "purple", "VERY BAD"
    elif air_index >= 300:
        return "brown", "DANGEROUS"


def get_last_update():
    return dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


container = st.container()
col1, col2, col3 = container.columns(3)
with col1:
    color, description = get_color_and_description(air_index)
    st.markdown(f"""<h6>🌫️ Air Quality Index</h6>""",
                unsafe_allow_html=True)
    st.markdown(
        f"""<h2 style="color:{color};">{air_index}</h2>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<h6> ☢️ Risk level</h6>""",
                unsafe_allow_html=True)
    st.markdown(
        f"""<h2 style="color:{color};">{description}</h2>""", unsafe_allow_html=True)
with col3:
    st.markdown(f" 📥 Last update : ``{get_last_update()}``")
    st.markdown(
        f"📢 Source : [Air Quality](https://open-meteo.com/en/docs/air-quality-api)")

with st.expander("📜 Air Index Details 🔽", expanded=False):
    # st.markdown("""<table>  <tr>    <th>IAQ</th>    <th>Niveau de risque</th>    <th>Impact sur la santé</th>  </tr>  <tr>    <td style="color:green;">0 - 50</td>    <td style="color:green;">Bon</td>    <td style="color:green;">La qualité de l'air est jugée satisfaisante, et la pollution de l'air pose peu ou pas de risque.</td>  </tr>  <tr>    <td style="color:yellow;">51 - 100</td>    <td style="color:yellow;">Modéré</td>    <td style="color:yellow;">La qualité de l'air est acceptable. Cependant, pour certains polluants, il peut y avoir un risque sur la santé pour un très petit nombre de personnes inhabituellement sensibles à la pollution atmosphérique.</td>  </tr>  <tr>    <td style="color:orange;">101 - 150</td>    <td style="color:orange;">Mauvais pour les groupes sensibles</td>    <td style="color:orange;">La qualité de l'air est acceptable; Cependant, pour certains polluants, il peut y avoir un problème de santé modérée pour un très petit nombre de personnes qui sont particulièrement sensibles à la pollution de l'air.</td>  </tr>  <tr>    <td style="color:red;">151 - 200</td>    <td style="color:red;">Mauvais</td>    <td style="color:red;">Tout le monde peut commencer à ressentir des effets sur la santé; les membres des groupes sensibles peuvent ressentir des effets de santé plus graves.</td>  </tr>  <tr>    <td style="color:purple;">201 - 300</td>    <td style="color:purple;">Très mauvais</td>    <td style="color:purple;">Avertissements de santé de conditions d'urgence. Toute la population est plus susceptible d'être affecté.</td>  </tr>  <tr>    <td style="color:brown;">300+</td>  <td style="color:brown;">Dangereux</td>    <td style="color:brown;">Alerte de santé: tout le monde peut ressentir des effets de santé plus graves.</td>  </tr></table>""",
    #             unsafe_allow_html=True)
    st.markdown("""<table class="infoaqitable"><thead><tr><td _msthash="1108679" _msttexthash="22880">AQI</td><td _msthash="1108680" _msttexthash="358059">Air pollution level </td><td _msthash="1108681" _msttexthash="258414">Impact on health</td></tr></thead><tbody><tr style="background-color:#009966;color:white"><td nowrap="true" _msthash="1116258" _msttexthash="21489">0 - 50</td><td _msthash="1116259" _msttexthash="43992">Good</td><td _msthash="1116260" _msttexthash="4023500">Air quality is considered satisfactory, and air pollution poses little or no risk.</td></tr><tr style="background-color:#ffde33"><td nowrap="true" _msthash="1116261" _msttexthash="35906">51 -100</td><td _msthash="1116262" _msttexthash="112801">Moderate</td><td _msthash="1116263" _msttexthash="14112332">Air quality is acceptable. However, for some pollutants, there may be a health risk for a very small number of people who are unusually sensitive to air pollution.</td></tr><tr style="background-color:#ff9933;color:white"><td nowrap="true" _msthash="1116264" _msttexthash="44421">101-150</td><td _msthash="1116265" _msttexthash="506857">Bad for sensitive groups</td><td _msthash="1116266" _msttexthash="16989310">Air quality is acceptable; However, for some pollutants, there may be a moderate health problem for a very small number of people who are particularly sensitive to air pollution. </td></tr><tr style="background-color:#cc0033;color:white"><td nowrap="true" _msthash="1116267" _msttexthash="44304">151-200</td><td _msthash="1116268" _msttexthash="27794">Bad</td><td _msthash="1116269" _msttexthash="7882524">Anyone can begin to experience health effects; Members of sensitive groups may experience more severe health effects.</td></tr><tr style="background-color:#660099;color:white"><td nowrap="true" _msthash="1116270" _msttexthash="44018">201-300</td><td _msthash="1116271" _msttexthash="93444">Very bad</td><td _msthash="1116272" _msttexthash="5060536">Health warnings of emergency conditions. The entire population is more likely to be affected. </td></tr><tr style="background-color:#7e0023;color:white"><td nowrap="true" _msthash="1116273" _msttexthash="20839">300+</td><td _msthash="1116274" _msttexthash="137241">Dangerous</td><td _msthash="1116275" _msttexthash="2613572">Health alert: Anyone can experience more serious health effects.</td></tr></tbody></table>""",
                unsafe_allow_html=True)

parameters = st.multiselect(
    "Select parameters", labels, "European Air Quality Index AQI")

# date input
col1, col2 = st.columns(2)
start_date = col1.date_input("Start date")
end_date = col2.date_input("End date")

if parameters:
    # Get the data
    df = get_data(start_date, end_date)
    if df is not None:
        # Plot the data
        st.line_chart(df.loc[:, parameters],
                      use_container_width=True, height=400, width=0)
    else:
        st.warning("No data available for the selected dates")
else:
    st.warning("Please select parameters to plot")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© COPYRIGHT 2023 - All Rights Reserved", unsafe_allow_html=True)