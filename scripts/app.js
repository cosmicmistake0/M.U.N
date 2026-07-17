var map = L.map("map");
map.fitBounds([
  [0.483, -2.8],
  [17.517, 18.233],
]);
imageBounds = [
  [
    [0.483, -2.8],
    [17.517, 18.233],
  ],
];
let hour = "f000";
let variable = "temperature";

let imageUrl = `/backend/data/20260711/overlays/${variable}_${hour}.png`;
let weather = L.imageOverlay(imageUrl, imageBounds, {
  opacity: 0.6,
}).addTo(map);
var osm = L.tileLayer(
  "https://tiles.stadiamaps.com/tiles/stamen_toner_dark/{z}/{x}/{y}{r}.{ext}",
  {
    minZoom: 0,
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
