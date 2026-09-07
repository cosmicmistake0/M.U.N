const response = await fetch("/backend/data/20260711/forecast.json");
const forecast = await response.json();
const ctx = document.getElementById("chart");
const hours = ["f000", "f012", "f024", "f036", "f048", "f060", "f072"];

//getting Chart Data
let state = "Abuja";
function chartData() {
  const precipitation = [];
  const wind = [];
  const temperature = [];
  hours.forEach((hour) => {
    temperature.push(forecast[hour][state].temperature);

    precipitation.push(forecast[hour][state].precipitation);

    wind.push(forecast[hour][state].wind10m.speed);
  });

  return {
    hours,
    temperature,
    precipitation,
    wind,
  };
}
const data = chartData();

console.log(data);
new Chart(ctx, {
  type: "line",

  data: {
    labels: hours,

    datasets: [
      {
        label: "Temperature",
        data: data.temperature,
        yAxisID: "y",
        borderWidth: 1,
      },

      {
        label: "Precipitation",
        data: data.precipitation,
        yAxisID: "y1",
        borderWidth: 1,
      },

      {
        label: "Wind",
        data: data.wind,
        yAxisID: "y2",
        borderWidth: 1,
      },
    ],
  },

  options: {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Temperature (°C)",
        },
      },

      y1: {
        beginAtZero: true,
        position: "right",
        title: {
          display: true,
          text: "Precipitation (mm)",
        },
      },

      y2: {
        beginAtZero: true,
        position: "right",
        title: {
          display: true,
          text: "Wind (m/s)",
        },

        grid: {
          drawOnChartArea: false,
        },
      },
    },
  },
});
