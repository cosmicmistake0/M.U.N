import os

import datetime              
import matplotlib.pyplot as plt      
import cartopy, cartopy.crs as ccrs  
import numpy as np       
import pygrib     
import json


forecast = {}
states = {

   
    "Abia": {"lat": 5.53294, "lon": 7.49433},

  
    "Adamawa": {"lat": 9.20893, "lon": 12.48025},

    
    "Akwa Ibom": {"lat": 4.99008, "lon": 7.91473},

    
    "Anambra": {"lat": 6.21895, "lon": 7.07744},

    
    "Bauchi": {"lat": 11.01370, "lon": 9.88625},

     
    "Bayelsa": {"lat":  5.06532, "lon": 6.35700},

   
    "Benue": {"lat": 7.73714, "lon": 8.51782},

     
    "Borno": {"lat": 11.83347, "lon": 13.13015},

    
    "Cross River": {"lat": 4.97960, "lon": 8.33736},

    
    "Delta": {"lat": 6.1858, "lon": 6.72971},

    
    "Ebonyi": {"lat": 6.2613, "lon": 8.22774},

     
    "Edo": {"lat": 6.33306, "lon": 5.62211},

    
    "Ekiti": {"lat":  7.60575, "lon": 5.25286},

     
    "Enugu": {"lat":  6.51450, "lon": 7.41753},

     
    "FCT": {"lat": 9.06590, "lon": 7.47208},

     
    "Gombe": {"lat":  9.66151, "lon": 11.49170},

     
    "Imo": {"lat":5.48974, "lon":7.03420},

     
    "Jigawa": {"lat": 11.80712, "lon": 9.30993},

     
    "Kaduna": {"lat": 10.26472, "lon": 7.45503},

    
    "Kano": {"lat": 11.99400, "lon": 8.5219},

   
    "Katsina": {"lat": 12.23787, "lon": 7.94967},
 
    "Kebbi": {"lat":12.47504, "lon": 4.26391},

    
    "Kogi": {"lat": 8.23487, "lon": 6.45264},

     
    "Kwara": {"lat":  8.49637, "lon": 4.54805},

     
    "Lagos": {"lat":  6.60487, "lon": 3.34666},

     
    "Nasarawa": {"lat":  8.71136, "lon":8.62427},

     
    "Niger": {"lat": 9.61871, "lon": 6.54758},

     
    "Ogun": {"lat": 7.16100, "lon": 3.34800},

     
    "Ondo": {"lat": 7.25256, "lon": 5.19326},

     
    "Osun": {"lat": 7.75983, "lon": 4.56625},

     
    "Oyo": {"lat": 7.37861, "lon":3.89699},

     
    "Plateau": {"lat": 9.91751, "lon": 8.89794},

    
    "Rivers": {"lat": 4.76862, "lon": 7.00923},

    
    "Sokoto": {"lat": 12.71071, "lon": 5.48044},

    
    "Taraba": {"lat":  8.90675, "lon": 11.3384},

     
    "Yobe": {"lat": 11.74700, "lon": 11.96080},

     
    "Zamfara": {"lat": 12.00136, "lon":6.84302},
}

date = datetime.datetime.now().strftime("%Y%m%d")
folder = f"C:/Users/USER/Desktop/M.U.N/backend/data/20260711"
# overlay_folder = f"{folder}/overlays"

# os.makedirs(overlay_folder, exist_ok=True)
def cardinal(deg):
    directions = [
        "N", "NE", "E", "SE",
        "S", "SW", "W", "NW"
    ]
    return directions[round(deg / 45) % 8]
def create_state_values(path, value, forecast_hour, forecast):

    grib = pygrib.open(path)

    grb = grib.select(name=value["variable"])[0]

    extent = [-2.8, 18.233, 0.483, 17.517]

    data, lats, lons = grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    data = data + value["offset"]

    for state, coords in states.items():

        city_lat = coords["lat"]
        city_lon = coords["lon"]

        row = np.abs(lats[:, 0] - city_lat).argmin()
        col = np.abs(lons[0, :] - city_lon).argmin()

        weather_value = float(data[row, col])
        
        
        if state not in forecast[forecast_hour]:
            forecast[forecast_hour][state] = {}

       
        forecast[forecast_hour][state][value["name"]] = weather_value

    grib.close()

def create_10wind_overlay(path,  forecast_hour, forecast):

    grib = pygrib.open(path)

    u_grb = grib.select(
        name="10 metre U wind component",
      
    )[0]

    v_grb = grib.select(
        name="10 metre V wind component",
        
    )[0]

    extent = [-2.8, 18.233, 0.483, 17.517]

    u, lats, lons = u_grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    v, _, _ = v_grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    data = np.sqrt(u**2 + v**2)

    for state, coords in states.items():

        city_lat = coords["lat"]
        city_lon = coords["lon"]

        row = np.abs(lats[:, 0] - city_lat).argmin()
        col = np.abs(lons[0, :] - city_lon).argmin()
        u_comp=u[row, col]
        v_comp=v[row, col]
        speed = float(data[row, col])
        direction=(270-(np.degrees(np.arctan2(v_comp, u_comp))))%360
        cardinal_direction = cardinal(direction)
       
       
        forecast[forecast_hour][state]["10M wind"] = {
        "speed": speed,
        "direction": direction,
        
        "cardinal":cardinal_direction
        }

    grib.close()
    
def create_upper_wind_values(path, level, forecast_hour, forecast):

    grib = pygrib.open(path)

    u_grb = grib.select(
        name="U component of wind",
        level=level
    )[0]

    v_grb = grib.select(
        name="V component of wind",
        level=level
    )[0]

    extent = [-2.8, 18.233, 0.483, 17.517]

    u, lats, lons = u_grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    v, _, _ = v_grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    wind_speed = np.sqrt(u**2 + v**2)

    for state, coords in states.items():

        city_lat = coords["lat"]
        city_lon = coords["lon"]

        row = np.abs(lats[:, 0] - city_lat).argmin()
        col = np.abs(lons[0, :] - city_lon).argmin()

        u_comp = u[row, col]
        v_comp = v[row, col]

        speed = float(wind_speed[row, col])
        direction = (270 - np.degrees(np.arctan2(v_comp, u_comp))) % 360
        cardinal_direction = cardinal(direction)
        

        forecast[forecast_hour][state][f"wind{level}"] = {
            "speed": speed,
            "direction": direction,
            "cardinal":cardinal_direction
        }

    grib.close()    

values = [

    {
        "name": "temperature",
        "variable": "2 metre temperature",
        "offset": -273.15
    },

    {
        "name": "precipitation",
        "variable": "Total Precipitation",
        "offset": 0
    }

]

forecast_hours = [
    "f000",
    "f012",
    "f024",
    "f036",
    "f048",
    "f060",
    "f072"
]
for forecast_hour in forecast_hours:

    path = f"{folder}/gfs_{forecast_hour}.grib2"

    forecast[forecast_hour] = {}

    for value in values:

        if forecast_hour == "f000" and value["name"] == "precipitation":
            continue

        create_state_values(
            path,
            value,
            forecast_hour,
            forecast
        )

    create_10wind_overlay(
        path,
        forecast_hour,
        forecast
    )

    create_upper_wind_values(
        path,
        850,
        forecast_hour,
        forecast
    )

    create_upper_wind_values(
        path,
        700,
        forecast_hour,
        forecast
    )


with open(f"{folder}/forecast.json", "w") as file:
    json.dump(forecast, file, indent=4)  