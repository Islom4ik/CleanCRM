var dataset = chart_datas

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
        .range(["#BFDBFE", "#60A5FA", "#2563EB"]);

    var svg = d3
        .select("#chart1")
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