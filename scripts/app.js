import { chartData } from "./graph.js";
const response = await fetch("/backend/data/20260711/forecast.json");
const forecast = await response.json();
var map = L.map("map");
const forecastHour = ["f000", "f012", "f024", "f036", "f048", "f060"];

map.fitBounds([
  [0.483, -2.8],
  [17.517, 18.233],
]);
let imageBounds = [
  [
    [0.483, -2.8],
    [17.517, 18.233],
  ],
];
map.setMaxBounds(imageBounds);
let hour = "f000";
let variable = "temperature";

let imageUrl = `/backend/data/20260711/overlays/${variable}_${hour}.png`;
let weather = L.imageOverlay(imageUrl, imageBounds, {
  opacity: 0.6,
}).addTo(map);

var osm = L.tileLayer(
  "https://tiles.stadiamaps.com/tiles/stamen_toner_background/{z}/{x}/{y}{r}.{ext}",

  {
    minZoom: 6,
    maxZoom: 20,
    attribution:
      '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    ext: "png",
  },
);

const time = document.querySelectorAll("[id=time]");
const variable_overlay = document.querySelectorAll("[id=variable]");
variable_overlay.forEach((button) => {
  button.addEventListener("click", () => {
    variable = button.dataset.variable;

    imageUrl = `/backend/data/20260711/overlays/${variable}_${hour}.png`;

    overlay();
  });
});
time.forEach((button) => {
  button.addEventListener("click", () => {
    hour = button.dataset.hour;
    console.log(hour);
    imageUrl = `/backend/data/20260711/overlays/${variable}_${hour}.png`;

    overlay();
  });
});

function overlay() {
  weather.setUrl(imageUrl);
}

osm.addTo(map);
// for weather forecast

const forecastHtml = document.getElementById("forecast-panel");

function showForecast(state) {
  let html = `
        <div class="state">
            <h2>${state}</h2>
        </div>

        <div class="weather">
    `;

  for (let i = 0; i < forecastHour.length; i += 2) {
    const morning = forecast[forecastHour[i]][state];
    const evening = forecast[forecastHour[i + 1]]?.[state];

    html += `
            <div class="day">

                <h3 class="date">Day ${i / 2 + 1}</h3>

                <div class="forecast-period">
                    <h4 class="time">Morning</h4>
                    <p>Temperature: ${Math.round(morning.temperature)}°C</p>
                    <p>Rain: ${Math.round(morning.precipitation)} mm</p>
                    <p>Wind: ${morning.wind10m.cardinal} ${Math.round(morning.wind10m.speed)} m/s</p>
                </div>

                ${
                  evening
                    ? `
                    <div class="forecast-period">
                        <h4 class="time">Evening</h4>
                        <p>Temperature: ${Math.round(evening.temperature)}°C</p>
                        <p>Rain: ${Math.round(evening.precipitation)} mm</p>
                        <p>Wind: ${evening.wind10m.cardinal} ${Math.round(evening.wind10m.speed)} m/s</p>
                    </div>
                    `
                    : ""
                }

            </div>
        `;
  }

  html += `
        </div>
    `;

  forecastHtml.innerHTML = html;
}
showForecast("Abuja");
const capitals = {
  Umuahia: { lat: 5.53294, lon: 7.49433 },

  Yola: { lat: 9.20893, lon: 12.48025 },

  Uyo: { lat: 4.99008, lon: 7.91473 },

  Awka: { lat: 6.21895, lon: 7.07744 },

  Bauchi: { lat: 11.0137, lon: 9.88625 },

  Yenagoa: { lat: 5.06532, lon: 6.357 },

  Makurdi: { lat: 7.73714, lon: 8.51782 },

  Maiduguri: { lat: 11.83347, lon: 13.13015 },

  Calabar: { lat: 4.9796, lon: 8.33736 },

  Asaba: { lat: 6.1858, lon: 6.72971 },

  Abakaliki: { lat: 6.2613, lon: 8.22774 },

  "Benin City": { lat: 6.33306, lon: 5.62211 },

  "Ado-Ekiti": { lat: 7.60575, lon: 5.25286 },

  Enugu: { lat: 6.5145, lon: 7.41753 },

  Abuja: { lat: 9.0659, lon: 7.47208 },

  Gombe: { lat: 9.66151, lon: 11.4917 },

  Owerri: { lat: 5.48974, lon: 7.0342 },

  Dutse: { lat: 11.80712, lon: 9.30993 },

  Kaduna: { lat: 10.26472, lon: 7.45503 },

  Kano: { lat: 11.994, lon: 8.5219 },

  Katsina: { lat: 12.23787, lon: 7.94967 },

  "Birnin Kebbi": { lat: 12.47504, lon: 4.26391 },

  Lokoja: { lat: 8.23487, lon: 6.45264 },

  Ilorin: { lat: 8.49637, lon: 4.54805 },

  Ikeja: { lat: 6.60487, lon: 3.34666 },

  Lafia: { lat: 8.71136, lon: 8.62427 },

  Minna: { lat: 9.61871, lon: 6.54758 },

  Abeokuta: { lat: 7.161, lon: 3.348 },

  Akure: { lat: 7.25256, lon: 5.19326 },

  Osogbo: { lat: 7.75983, lon: 4.56625 },

  Ibadan: { lat: 7.37861, lon: 3.89699 },

  Jos: { lat: 9.91751, lon: 8.89794 },

  "Port Harcourt": { lat: 4.76862, lon: 7.00923 },

  Sokoto: { lat: 12.71071, lon: 5.48044 },

  Jalingo: { lat: 8.90675, lon: 11.3384 },

  Damaturu: { lat: 11.747, lon: 11.9608 },

  Gusau: { lat: 12.00136, lon: 6.84302 },
};
const majorCities = L.layerGroup();
const minorCities = L.layerGroup();
Object.entries(capitals).forEach(([city, coords]) => {
  const cities = L.marker([coords.lat, coords.lon], {
    icon: L.divIcon({
      className: "state-label",

      html: `<div data-capital="${city}">${city}</div>`,
    }),
  })

    .on("click", () => {
      showForecast(city);
      chartData(city);
    });
  if (
    city === "Ikeja" ||
    city === "Abuja" ||
    city === "kano" ||
    city === "Jos" ||
    city === "Sokoto" ||
    city === "Maiduguri" ||
    city === "Port Harciurt" ||
    city === "Enugu" ||
    city === "Benin City" ||
    city === "Calabar" ||
    city === "Yola" ||
    city === "Ibadan" ||
    city === "Kaduna" ||
    city === "Ilorin"
  ) {
    cities.addTo(majorCities);
  } else {
    cities.addTo(minorCities);
  }
});
majorCities.addTo(map);
majorCities.addTo(map);

map.on("zoomend", () => {
  if (map.getZoom() >= 6.5) {
    map.addLayer(minorCities);
  } else {
    map.removeLayer(minorCities);
  }
});

const windVarBtn = document.querySelectorAll(".wind-var");
const precipVarBtn = document.querySelector(".precip-var");
const tempVarBtn = document.querySelector(".temperature-var");

const tempLgd = document.querySelector(".temp");
const windLgd = document.querySelector(".wind");
const precipLgd = document.querySelector(".precip");

function tempLegend() {
  tempLgd.style.display = "block";
  windLgd.style.display = "none";
  precipLgd.style.display = "none";
}
function precipLegend() {
  tempLgd.style.display = "none";
  windLgd.style.display = "none";
  precipLgd.style.display = "block";
}
function windLegend() {
  tempLgd.style.display = "none";
  windLgd.style.display = "block";
  precipLgd.style.display = "none";
}
precipVarBtn.addEventListener("click", precipLegend);
tempVarBtn.addEventListener("click", tempLegend);
windVarBtn.forEach((button) => {
  button.addEventListener("click", windLegend);
});
