from dataFetchers import *

# Nice Coordinates
lat, lon = 43.70, 7.27 

# with open("openuv_tokens.txt") as f:
#     tokens = f.read().splitlines()

def airqualityHistory(start_date, end_date):
    airQuality = openMeteoAirQualityAPIFetcher(lat, lon, start_date, end_date)
    return airQuality

def weatherHistory(start_date, end_date):
    openMeteoWeather = openMeteoWeatherAPIFetcher(lat, lon, start_date, end_date)
    return openMeteoWeather

def marineHistory(start_date, end_date):
    openMeteoMarine = openMeteoMarineAPIFetcher(lat, lon, start_date, end_date)
    return openMeteoMarine

def uvHistory(start_date, end_date):
    openUV = openMeteoUVAPIFetcher(lat, lon, start_date, end_date)
    return openUV

if __name__ == "__main__":
    import json
    with open("data.json", "w") as f:
        json.dump(airqualityHistory("2023-01-01", "2023-01-15"), f, indent=4)
   
