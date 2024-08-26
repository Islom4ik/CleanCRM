const lead_input_phone = document.querySelectorAll('.lead_input_phone')
const lead_input_status = document.querySelectorAll('.lead_input_status')
const lead_input_product = document.querySelectorAll('.lead_input_product')
const lead_input_address = document.querySelectorAll('.lead_input_address')
const lead_input_callcount = document.querySelectorAll('.lead_input_callcount')
const lead_input_calldate = document.querySelectorAll('.lead_input_calldate')
const lead_input_soldprice = document.querySelectorAll('.lead_input_soldprice')
const lead_input_soldcount = document.querySelectorAll('.lead_input_soldcount')
const lead_edit_submit = document.querySelectorAll('.lead_edit_submit')
const lead_input_comment = document.querySelectorAll('.lead_input_comment')
const background_loader = document.querySelector('.background-loader')
const header = document.querySelector('header')
const rob_lead_checkboxes = document.querySelectorAll('.rob_lead_checkbox')

const send_leads_div_button = document.querySelector('.send_leads_div-button')
const send_leads_div_for = document.getElementById('send_leads_div_for')
const comments_section = document.querySelectorAll('.comments_section')
const comments_pop_up = document.querySelectorAll('.comments_pop-up')

window.onload = function() {
  background_loader.style.opacity = 0
  background_loader.style.pointerEvents = 'none';
  setTimeout(() => {
    background_loader.style.display = 'None'
  }, 2000);
};

try {
  send_leads_div_button.addEventListener('click', async (e) => {
    background_loader.style.display = 'flex'
    background_loader.style.opacity = 1
    var operator_pk = Number(send_leads_div_for.value)
    var leads = []
    rob_lead_checkboxes.forEach(element => {
      if (element.checked) {
        leads.push(Number(element.id))
      }
    })
    console.log(leads);
    
    console.log(csrf_token);
    if (leads.length == 0) {
      alert('Chose leads')
      return location.reload()
    }
    
    
    
  
    var request = await fetch(`${window.location.origin}/api/operatorleads/post/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token
      },
      body: JSON.stringify({leads: leads, operator: operator_pk})
    })
  
    var data = await request.json()
    console.log(data);
    
    if (request.status == 200) return location.reload()
  })  
} catch (error) {console.log(error);}


comments_pop_up.forEach(element => {
  element.addEventListener('click', (e) => {
    var id = element.id
    for (let i = 0; i < comments_section.length; i++) {
      if (comments_section[i].id == id) {
        if (comments_section[i].style.display == 'none') comments_section[i].style.display = 'block'
        else comments_section[i].style.display = 'none'
        break
      }
    }
  })
})



try {
  rob_lead_checkboxes.forEach(element => {
    element.addEventListener('change', (e) => {
      element.setAttribute('checked', null)
    })
  })
} catch (error) {console.log(error);}


function formatDateIso(isoString) {
  const date = new Date(isoString);

  const day = date.getDate();
  const month = date.toLocaleString('en-US', { month: 'short' }); // "Aug"
  const year = date.getFullYear();
  let hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const ampm = hours >= 12 ? 'p.m.' : 'a.m.'; // Используем "p.m." и "a.m."
  hours = hours % 12 || 12; // Переключение на 12-часовой формат

  return `${month}. ${day}, ${year}, ${hours}:${minutes} ${ampm}`;
}

lead_input_comment.forEach(element => {
  element.addEventListener('keydown', async function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        if (element.value.trim() == '') return element.value = '' 
        var lead_pk = Number(element.id)
        console.log(lead_pk);
        console.log(element.value);
        var request = await fetch(`${window.location.origin}/api/comment/add/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
          },
          body: JSON.stringify({owner: account_pk, text: element.value, lead: lead_pk})
        })
      
        var data = await request.json()
        console.log(data); 

        comments_section.forEach(comments_div => {
          if (comments_div.id == element.id) {
            var date = formatDateIso(data.comment.upload_date)
            comments_div.innerHTML += `\n<div class="comments_section-comment" style="text-align: start; margin-top: 20px;">
                                <div class="comments_section-comment-owner_info" style="display: flex; align-items: center;">
                                    <img src="${data.commentator.avatar}" alt="" style="width: 30px; height: 30px; border-radius: 50%; margin-right: 5px;">
                                    <span style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; font-size: 16px;">${data.commentator.first_name} | ${data.commentator.role} (${date}):</span>
                                </div>
                                <p class="comments_section-comment-text" style="font-weight: 400; margin-top: 5px; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; font-size: 18px;">${data.comment.text}</p>
                            </div>`
          }
          
          comments_div.style.display = 'block'

          comments_div.scrollTo({
            top: comments_div.scrollHeight,
            behavior: 'smooth'
          });

        })

        comments_pop_up.forEach(comment_pop_up => {
          if (comment_pop_up.id == element.id) {
            comment_pop_up.innerHTML = `${data.comments_count} comments`
          }
        })

        element.value = '' 
    }
  });
})


lead_edit_submit.forEach(button => {
  button.addEventListener('click', async (e) => {
    await e.preventDefault()
    var lead_pk = Number(button.id)
    console.log(lead_pk);
    
    var lead_phone = ''
    var lead_status = ''
    var lead_product = ''
    var lead_address = ''
    var lead_soldcount = ''
    var lead_soldprice = ''
    var lead_callcount = ''
    var lead_calldate = ''
    lead_input_phone.forEach(phone => {
      if (phone.id == lead_pk) lead_phone = phone.value
    })
    lead_input_status.forEach(status => {
      if (status.id == lead_pk) lead_status = status.value
    })
    lead_input_product.forEach(product => {
      if (product.id == lead_pk) lead_product = product.value
    })
    lead_input_address.forEach(address => {
      if (address.id == lead_pk) lead_address = address.value
    })
    lead_input_soldcount.forEach(soldcount => {
      if (soldcount.id == lead_pk) lead_soldcount = soldcount.value || null
    })
    lead_input_soldprice.forEach(soldprice => {
      if (soldprice.id == lead_pk) lead_soldprice = soldprice.value || null
    })
    lead_input_callcount.forEach(callcount => {
      if (callcount.id == lead_pk) lead_callcount = callcount.value || null
    })
    lead_input_calldate.forEach(calldate => {
      if (calldate.id == lead_pk) lead_calldate = calldate.value || null
    })


    var solddate = null
    if (lead_status == 'Approved') {
      const today = new Date();

      const day = String(today.getDate()).padStart(2, '0'); // Получаем день и добавляем ведущий ноль, если нужно
      const month = String(today.getMonth() + 1).padStart(2, '0'); // Получаем месяц (getMonth() возвращает месяцы от 0 до 11, поэтому добавляем 1)
      const year = today.getFullYear();
      solddate = `${day}/${month}/${year}`
    }
    console.log(lead_phone);
    console.log(lead_status);
    console.log(lead_product);
    console.log(lead_address);
    console.log(lead_soldcount);
    console.log(lead_soldprice);
    console.log(lead_callcount);
    console.log(lead_calldate);
    var request = await fetch(`${window.location.origin}/api/leads/edit/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token
      },
      body: JSON.stringify({pk: lead_pk, lead_phone: lead_phone, lead_status: lead_status, lead_product: lead_product, lead_address: lead_address, lead_soldcount: lead_soldcount, lead_soldprice: Number(lead_soldprice), lead_callcount: Number(lead_callcount), lead_calldate: lead_calldate, solddate: solddate})
    })
  
    var data = await request.json()
    console.log(data);
    
    location.reload()
  })
})




// $(function () {
//     $(document.getElementById("datepicker")).datepicker({ firstDay: 1 });
//     });

//     $("#datepicker").datepicker({
//     onSelect: function() { 
//         var dateObject = $(this).datepicker('getDate');
//         var ThisDay = dateObject.getDate();
//         var ThisMonth = dateObject.getMonth();
//         var ThisYear = dateObject.getFullYear();
//         var date_str = `${ThisDay}/${ThisMonth}/${ThisYear}`
//         console.log(date_str); 
//     }
// });


// Chart js

var dataset = statuses_dataset;
  
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

  