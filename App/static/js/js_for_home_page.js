function write_list() {
    function getdate() {
        var regexp;
        regexp = /(\d{4}\-\d{1,2})\-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}\.\d{1,6}/;
        var first_date = document.getElementById('first_date').value;
        var second_date = document.getElementById('second_date').value;
        var a = document.getElementById('first_event');
        var b = document.getElementById('second_event');
        var c = document.getElementById('third_event');
        var event_array = [a, b, c];
        var end_array = [];
        var i;
        for (i = 0; i < event_array.length; i++) {
            if (event_array[i].checked) {
                end_array.push(event_array[i].nextSibling.textContent)
            }
        }
        if (regexp.test(first_date) && regexp.test(second_date)) {
            var date_array;
            date_array = [first_date, second_date];
        }
        return [date_array, end_array];
    }

    function draw() {
        new Chartist.Bar('#myChart', {
            labels: ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
            series: [20, 60, 120, 200, 180, 20, 10]
        }, {
            distributeSeries: true
        });
    }

    elem = getdate();
    if (elem[0] != null) {
        var date_from = elem[0][0];
        var date_to = elem[0][1]
    }
    if (elem[1] != null) {
        var event = elem[1][0]
    }
    var xmlhttp = null;
    if (window.XMLHttpRequest)
        xmlhttp = new XMLHttpRequest();
    else
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange = function () {

        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var row = '';

            var response =  JSON.parse(xmlhttp.response);
            console.log(response)

            //var response = response_list.a
            for (var i in response) {
                row += '<a href="#" class="list-group-item">' + '[' + response[i].Time.$date + ']' + ' ' + '[' + response[i].UID + ']' + ' ' + '[' +response[i].Event+ ']' + '<br>';
            }

            document.getElementById("list-group").innerHTML = row;

        }
    }
        ;
        draw();
        if (date_from != null && date_to != null)
            xmlhttp.open("get", "/get?date_from=" + date_from + "&date_to=" + date_to + "&event=" + event, true);
        else
            xmlhttp.open("get", "/get?event=" + event, true);
        xmlhttp.send();

    }
google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawLineColors);
function drawLineColors() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'X');
      data.addColumn('number', 'Dogs');
      data.addColumn('number', 'Cats');

      data.addRows([
        [0, 0, 0],    [1, 10, 5],   [2, 23, 15],  [3, 17, 9],   [4, 18, 10],  [5, 9, 5],
        [6, 11, 3],   [7, 27, 19],  [8, 33, 25],  [9, 40, 32],  [10, 32, 24], [11, 35, 27],
        [12, 30, 22], [13, 40, 32], [14, 42, 34], [15, 47, 39], [16, 44, 36], [17, 48, 40],
        [18, 52, 44], [19, 54, 46], [20, 42, 34], [21, 55, 47], [22, 56, 48], [23, 57, 49],
        [24, 60, 52], [25, 50, 42], [26, 52, 44], [27, 51, 43], [28, 49, 41], [29, 53, 45],
        [30, 55, 47], [31, 60, 52], [32, 61, 53], [33, 59, 51], [34, 62, 54], [35, 65, 57],
        [36, 62, 54], [37, 58, 50], [38, 55, 47], [39, 61, 53], [40, 64, 56], [41, 65, 57],
        [42, 63, 55], [43, 66, 58], [44, 67, 59], [45, 69, 61], [46, 69, 61], [47, 70, 62],
        [48, 72, 64], [49, 68, 60], [50, 66, 58], [51, 65, 57], [52, 67, 59], [53, 70, 62],
        [54, 71, 63], [55, 72, 64], [56, 73, 65], [57, 75, 67], [58, 70, 62], [59, 68, 60],
        [60, 64, 56], [61, 60, 52], [62, 65, 57], [63, 67, 59], [64, 68, 60], [65, 69, 61],
        [66, 70, 62], [67, 72, 64], [68, 75, 67], [69, 80, 72]
      ]);

      var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Popularity'
        },
        colors: ['#a52714', '#097138']
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawPieChart() {

    var data = google.visualization.arrayToDataTable([
        ['Task', 'Hours per Day'],
        ['Work',     11],
        ['Eat',      2],
        ['Commute',  2],
        ['Watch TV', 2],
        ['Sleep',    7]
    ]);

    var options = {
        title: 'My Daily Activities'
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}