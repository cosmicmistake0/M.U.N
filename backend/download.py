import datetime
import requests
import os

date = datetime.datetime.now().strftime("%Y%m%d")
print(date)

folder = f"C:/Users/USER/Desktop/M.U.N/backend/data/{date}"
os.makedirs(folder, exist_ok=True)

forecast_hours = ["f000","f012", "f024","f036", "f048", "f060","f072"]

for forecast_hour in forecast_hours:

    url = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.{forecast_hour}&all_var=on&all_lev=on&subregion=&toplat=17.517&leftlon=-2.8&rightlon=18.233&bottomlat=0.483"

    r = requests.get(url)

    if r.status_code == 200:
        with open(f"{folder}/gfs_{forecast_hour}.grib2", "wb") as fp:
            fp.write(r.content)

        print(f"Downloaded gfs_{forecast_hour}.grib2")

    else:
        print(f"Download failed: {r.status_code}")