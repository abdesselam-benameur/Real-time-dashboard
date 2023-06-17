from pymongo import MongoClient
from dataFetchers import *
from dataFill import fillData
import datetime

# Fill Real Time Data
def fillRealTimeData(real_time_db, mongo_client, tokens, lat, lon):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    openmeteo_args = [lat, lon, today_date, today_date] 
    openuv_args = [tokens.pop(), lat, lon] 
    configurations = {
        "openMeteoWeather": (openMeteoWeatherAPIFetcher, openmeteo_args),
        "openMeteoMarine": (openMeteoMarineAPIFetcher, openmeteo_args),
        "airQuality": (openMeteoAirQualityAPIFetcher, openmeteo_args),
        "openUV": (fetch_openuv_data, openuv_args)
    }
    fillData(real_time_db, mongo_client, tokens, configurations)

if __name__ == "__main__":
    mongo_client = MongoClient()
    # Nice Coordinates
    lat, lon = 43.70, 7.27

    with open("openuv_tokens.txt") as f:
        tokens = f.read().splitlines()

    fillRealTimeData("Temp_db", mongo_client, tokens, lat, lon)
    mongo_client.close()