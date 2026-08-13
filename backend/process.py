
import os

import datetime              
import matplotlib.pyplot as plt      
import cartopy, cartopy.crs as ccrs  
import numpy as np       
import pygrib       


date = datetime.datetime.now().strftime("%Y%m%d")
folder = f"C:/Users/USER/Desktop/M.U.N/backend/data/{date}"
overlay_folder = f"{folder}/overlays"

os.makedirs(overlay_folder, exist_ok=True)

def create_overlay(path, overlay, forecast_hour):

    grib = pygrib.open(path)

    grb = grib.select(name=overlay["variable"])[0]

    extent = [-2.8, 18.233, 0.483, 17.517]

    data, lats, lons = grb.data(
        lat1=extent[2],
        lat2=extent[3],
        lon1=extent[0],
        lon2=extent[1]
    )

    
    data = data + overlay["offset"]

    plt.figure(figsize=(10, 6), dpi=400)

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.spines["geo"].set_visible(False)
    ax.patch.set_visible(False)

    ax.contourf(
        lons,
        lats,
        data,
        levels=overlay["levels"],
        cmap=overlay["cmap"],
        transform=ccrs.PlateCarree()
    )

    plt.savefig(
        f"{overlay_folder}/{overlay['name']}_{forecast_hour}.png",
        bbox_inches="tight",
        transparent=True,
        extend="max",
        pad_inches=0
    )

    plt.close()
    grib.close()

overlays = [

    {
        "name": "temperature",
        "variable": "2 metre temperature",
        "cmap": "hot",
        "levels": np.arange(10,40
        ,2),
      
        "offset": -273.15
    },

    {
        "name": "precipitation",
        "variable": "Total Precipitation",
        "cmap": "turbo",
        "levels": [0,0.1,0.5,1,2,5,10,20,50,100],
       
        "offset": 0
    }

]




def create_wind_overlay(path, level, filename):

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

    plt.figure(figsize=(10,6), dpi=400)

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.spines["geo"].set_visible(False)
    ax.patch.set_visible(False)

    levels = np.arange(0,30,1)

    ax.contourf(
        lons,
        lats,
        wind_speed,
        levels=levels,
        cmap="viridis",
        transform=ccrs.PlateCarree()
    )

    u_norm = np.divide(
        u,
        wind_speed,
        out=np.zeros_like(u),
        where=wind_speed!=0
    )

    v_norm = np.divide(
        v,
        wind_speed,
        out=np.zeros_like(v),
        where=wind_speed!=0
    )

    skip = 5

    ax.quiver(
        lons[::skip,::skip],
        lats[::skip,::skip],
        u_norm[::skip,::skip],
        v_norm[::skip,::skip],
        transform=ccrs.PlateCarree(),
        pivot="middle"
    )

    plt.savefig(
        filename,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True
    )
    grib.close()
    plt.close()

def create_10wind_overlay(path,  filename):

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

    wind_speed = np.sqrt(u**2 + v**2)

    plt.figure(figsize=(10,6), dpi=400)

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.spines["geo"].set_visible(False)
    ax.patch.set_visible(False)

    levels = np.arange(0,30,1)

    ax.contourf(
        lons,
        lats,
        wind_speed,
        levels=levels,
        cmap="viridis",
        transform=ccrs.PlateCarree()
    )

    u_norm = np.divide(
        u,
        wind_speed,
        out=np.zeros_like(u),
        where=wind_speed!=0
    )

    v_norm = np.divide(
        v,
        wind_speed,
        out=np.zeros_like(v),
        where=wind_speed!=0
    )

    skip = 5

    ax.quiver(
        lons[::skip,::skip],
        lats[::skip,::skip],
        u_norm[::skip,::skip],
        v_norm[::skip,::skip],
        transform=ccrs.PlateCarree(),
        pivot="middle"
    )

    plt.savefig(
        filename,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True
    )
    grib.close()
    plt.close()   
     
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

    create_overlay(path, overlays[0], forecast_hour)   # temperature

    if forecast_hour != "f000":
        create_overlay(path, overlays[1], forecast_hour)   # precipitation

    create_wind_overlay(
        path,
        850,
        f"{overlay_folder}/wind850_{forecast_hour}.png"
    )

    create_wind_overlay(
        path,
        700,
        f"{overlay_folder}/wind700_{forecast_hour}.png"
    )

    create_10wind_overlay(
        path,
        f"{overlay_folder}/wind_10m_{forecast_hour}.png"
    )