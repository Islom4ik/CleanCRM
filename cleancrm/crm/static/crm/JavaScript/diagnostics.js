
function getMonthsUntil(month) {
    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    const index = months.indexOf(month);
    if (index === -1) {
        throw new Error("Invalid month name");
    }
    let start = index - 5;
    if (start < 0) {
        return [...months.slice(12 + start), ...months.slice(0, index + 1)];
    }
    return months.slice(start, index + 1);
}


function getMonthNameByIndex(index) {
    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    if (index < 0 || index > 11) {
        throw new Error("Invalid index. Please provide a value between 0 and 11.");
    }

    return months[index];
}

const now = new Date();
const monthIndex = now.getMonth();


  const labels = getMonthsUntil(getMonthNameByIndex(monthIndex));
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Profit mln sum",
        backgroundColor: "hsl(252, 82.9%, 67.8%)",
        borderColor: "hsl(252, 82.9%, 67.8%)",
        data: chart_profit_months,
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