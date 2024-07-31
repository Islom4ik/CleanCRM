
$(function () {
    $(document.getElementById("datepicker")).datepicker({ firstDay: 1 });
    });

    $("#datepicker").datepicker({
    onSelect: function() { 
        var dateObject = $(this).datepicker('getDate');
        var ThisDay = dateObject.getDate();
        var ThisMonth = dateObject.getMonth();
        var ThisYear = dateObject.getFullYear();
        var date_str = `${ThisDay}/${ThisMonth}/${ThisYear}`
        console.log(date_str); 
    }
});


// Chart js

var dataset = [
    { name: "Approved", count: 24 },
    { name: "New", count: 22 },
    { name: "Refused", count: 31 },
    { name: "Need_approved", count: 9 },
  ];
  
  var total = 0;
  
  dataset.forEach(function (d) {
    total += d.count;
  });
  
  var pie = d3.layout
    .pie()
    .value(function (d) {
      return d.count;
    })
    .sort(null);
  
  var w = 100, h = 100;
  
  var outerRadiusArc = w;
  var innerRadiusArc = 25;
  var shadowWidth = 5;
  var color = d3.scale
    .ordinal()
    .range(["#4ADE80", "#60A5FA", "#F87171", "#FACC15"]);
  
  var svg = d3
    .select("#chart")
    .append("svg")
    .attr({
      width: w,
      height: h,
      class: "shadow"
    })
    .append("g")
    .attr({
      transform: "translate(" + w / 2 + "," + h / 2 + ")"
    });
  
  var createChart = function (
    svg,
    outerRadius,
    innerRadius,
    fillFunction,
    className
  ) {
    var arc = d3.svg.arc().innerRadius(outerRadius).outerRadius(innerRadius);
  
    var path = svg
      .selectAll("." + className)
      .data(pie(dataset))
      .enter()
      .append("path")
      .attr({
        class: className,
        d: arc,
        fill: fillFunction
      });
  
    path
      .transition()
      .duration(1000)
      .attrTween("d", function (d) {
        var interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
        return function (t) {
          return arc(interpolate(t));
        };
      });
  };
  
  createChart(
    svg,
    outerRadiusArc,
    innerRadiusArc,
    function (d, i) {
      return color(d.data.name);
    },
    "path1"
  );
  
  createChart(
    svg,
    outerRadiusArcShadow,
    innerRadiusArcShadow,
    function (d, i) {
      var c = d3.hsl(color(d.data.name));
      return d3.hsl(c.h + 5, c.s - 0.07, c.l - 0.15);
    },
    "path2"
  );
  
  var restOfTheData = function () {
    addText(
      function () {
        return numberWithCommas(total);
      },
      0,
      "30px"
    );
  
    addText(
      function () {
        return "Page View";
      },
      25,
      "10px"
    );
  };
  
  setTimeout(restOfTheData, 1000);
  
  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }


  document.addEventListener("alpine:init", () => {
    Alpine.data("apex_app", () => ({
      values: [4000, 380, 340, 21, 2200, 1100, 100, 600, 80, 900, 10, 55],
      labels: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Maj",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Dec"
      ],
      init() {
        let chart = new ApexCharts(this.$refs.chart, this.options);
        chart.render();
        /* this.$watch("values", () => {
          chart.updateOptions(this.options);
        });*/
      },
      formatCurrency: (x) => {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " $";
      },
      get options() {
        return {
          series: [
            {
              name: "Series name",
              data: this.values
            }
          ],
          chart: {
            defaultLocale: "en",
            height: 350,
            type: "line",
            zoom: {
              enabled: true
            },
            dropShadow: {
              enabled: true,
              color: "#000",
              top: 18,
              left: 7,
              blur: 15,
              opacity: 0.3
            }
          },
          dataLabels: {
            enabled: true,
            textAnchor: "start",
            formatter: (val) => {
              return this.formatCurrency(val);
            },
            style: {
              colors: ["#4d78kl"]
            }
          },
          stroke: {
            show: true,
            curve: "smooth",
            lineCap: "butt",
            colors: "#222",
            width: 2,
            dashArray: 0
          },
          grid: {
            borderColor: "#DCDFE1",
            row: {
              opacity: 0.5
            }
          },
          yaxis: {
            title: {
              text: "Yaxis ($)"
            },
            labels: {
              formatter: (value) => {
                return this.formatCurrency(value);
              }
            }
          },
          xaxis: {
            title: {
              text: "Xaxis"
            },
            categories: this.labels
          },
          tooltip: {
            x: {
              show: true
            },
            y: {
              formatter: (val) => {
                return this.formatCurrency(val);
              }
            }
          },
          markers: {
            size: 7,
            colors: "pink",
            strokeColors: "#fff",
            strokeWidth: 2,
            strokeOpacity: 0.9,
            strokeDashArray: 0,
            fillOpacity: 1,
            discrete: [],
            shape: "circle",
            radius: 2,
            offsetX: 0,
            offsetY: 0,
            onClick: undefined,
            onDblClick: undefined,
            showNullDataPoints: true,
            hover: {
              size: undefined,
              sizeOffset: 3
            }
          },
          colors: ["pink"],
          dataLabels: {
            enabled: true,
            enabledOnSeries: undefined,
            formatter: (val) => {
              return this.formatCurrency(val);
            },
            textAnchor: "middle",
            offsetX: 10,
            offsetY: -10,
            style: {
              fontSize: "14px",
              fontFamily: "Helvetica, sans-serif",
              fontWeight: "500",
              colors: ["#222"]
            },
            background: {
              enabled: false
            },
            dropShadow: {
              enabled: true,
              top: 1,
              left: 1,
              blur: 1,
              color: "pink",
              opacity: 0.8
            }
          },
          legend: {
            position: "bottom",
            horizontalAlign: "left",
            floating: true,
            offsetY: -5,
            offsetX: -5,
            show: true,
            showForSingleSeries: true,
            customLegendItems: ["Actual"],
            markers: {
              fillColors: ["pink"]
            }
          }
        };
      }
    }));
  });

  