import requests
import datetime

def get_data(url, params=None, headers=None, start_date=None, end_date=None):
    if params is not None:
        url += "&".join(f"{key}={val}" for key, val in params.items()) 
    if start_date is not None and end_date is not None and not url.startswith("https://api.openuv.io"):
        url += f"&start_date={start_date}&end_date={end_date}"
    response = requests.get(url, headers=headers)
    data = response.json()
    # print(url)
    if response.status_code == 200:
        return data
    else:
        print(data)
        return None

# Open-Meteo Weather API
def openMeteoWeatherAPIFetcher(lat, lon, start_date=None, end_date=None):
    baseURL = "https://api.open-meteo.com/v1/forecast?"
    params = {
        "current_weather": True,
        "latitude": lat,
        "longitude": lon,
        "model": "meteofrance",
        "hourly": "temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,windspeed_10m",
        "timezone": "Europe/Paris" # "auto"
    }
    return get_data(baseURL, params=params, start_date=start_date, end_date=end_date)

# Open-Meteo Marine API
def openMeteoMarineAPIFetcher(lat, lon, start_date=None, end_date=None):
    baseURL = "https://marine-api.open-meteo.com/v1/marine?"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wave_height,wave_direction,wave_period"
    }
    return get_data(baseURL, params=params, start_date=start_date, end_date=end_date)

# Air Quality Index API
def openMeteoAirQualityAPIFetcher(lat, lon, start_date=None, end_date=None):
    baseURL = "https://air-quality-api.open-meteo.com/v1/air-quality?"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,european_aqi"
    }
    return get_data(baseURL, params=params, start_date=start_date, end_date=end_date)

# OpenUV API
def openUVAPIFetcher(token, lat, lon, alt=100, dt=None):
    baseURL = "https://api.openuv.io/api/v1/uv?"
    params = {
        "lat": lat,
        "lng": lon,
        "alt": alt
        # alt = Altitude.
        # Plus l'altitude augmente et moins il y a d'atmosphère pour absorber le rayonnement UV.
        # Tous les 1000 m de dénivelé, l'intensité des UV augmente de près de 10 %.
        # Source: Organisation mondiale de la Santé
        # https://www.who.int/fr/news-room/questions-and-answers/item/ultraviolet-(uv)-radiation
    }
    if dt is not None:
        params["dt"] = dt
    headers = {
        "x-access-token": token,
        "Content-Type": "application/json"
    }
    return get_data(baseURL, params=params, headers=headers)

# Open Meteo UV
def openMeteoUVAPIFetcher(lat, lon, start_date=None, end_date=None):
    baseURL = "https://air-quality-api.open-meteo.com/v1/air-quality?"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "uv_index"
    }
    return get_data(baseURL, params=params, start_date=start_date, end_date=end_date)

def fetch_openuv_data(token, lat, lon):
    data = []
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    for i in range(24):
        dt = f"{today_date}T{i:02}:00:00.000Z"
        data.append(openUVAPIFetcher(token, lat, lon, dt=dt))
    return data