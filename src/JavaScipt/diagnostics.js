
  const labels = ["January", "March", "April", "May", "June", "July"];
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Profit mln sum",
        backgroundColor: "hsl(252, 82.9%, 67.8%)",
        borderColor: "hsl(252, 82.9%, 67.8%)",
        data: [-10 , 0, 10, 15, 20, 25, 30],
      },
    ],
  };

  const configLineChart = {
    type: "line",
    data,
    options: {},
  };

  var chartLine = new Chart(
    document.getElementById("chartLine"),
    configLineChart
  );