function write_list() {;
    elem = getdate();
    var events = [];
    if (elem[0] != null) {
        var date_from = elem[0][0];
        var date_to = elem[0][1]
    }
    if (elem[1] != null) {
        elem[1].forEach(function (item) {
            events.push(item);
        })
    }
    var xmlhttp = null;
    var date_array = [];
    var count_array = [];
    var count_date_event_array = [];
    var rows_for_draw = [0];
    var events_array = [];
    var label_array =[];
    if (window.XMLHttpRequest)
        xmlhttp = new XMLHttpRequest();
    else
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

    xmlhttp.onreadystatechange = function () {

        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var row = '';
            var r = xmlhttp.response;
            var response = JSON.parse(r);
            var parsed_list = JSON.parse(response['a']);
            var parsed_stat = JSON.parse(response['b']);
            var date_str = ''
            parsed_stat.forEach(function (elem) {
                events_array.push(elem._id.Event)
            })
            function uniqueVal(value, index, self) {
                return self.indexOf(value) === index;
            }
            events_array = events_array.filter(uniqueVal);
            console.log(parsed_stat);
            for (var i in parsed_stat) {
                if ('hour' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.hour + ':~:~ ' + parsed_stat[i]._id.day + '.' + parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                } else if ('day' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.day + '.' + parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                } else if ('month' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                } else if ('year' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.year.toString().slice(-2);
                }
                date_array.push(date_str);
                count_date_event_array.push({"count" : parsed_stat[i].count,"date": date_str, "event": parsed_stat[i]._id.Event});
            }
            date_array = date_array.filter(uniqueVal);
            for (var i in parsed_list) {
                row += '<a href="#" class="list-group-item">' + '[' + parsed_list[i].Time.$date + ']' + ' ' + '[' + parsed_list[i].UID + ']' + ' ' + '[' + parsed_list[i].Event + ']' + '<br>';
            }
            document.getElementById("list-group").innerHTML = row;

        }
        function drawChart() {
            for (var i = 0; i < date_array.length; i++) {
                count_array.push([]);
                for (var j = 0; j < events_array.length; j++) {
                    count_array[i].push(0);
                }
            };
            for ( var i = 0; i < count_date_event_array.length;i++){
                for ( var j = 0; j < date_array.length; j++){
                    if ( count_date_event_array[i].date == date_array[j]){
                        for (var k = 0;k < events_array.length;k++){
                            if (count_date_event_array[i].event == events_array[k]){
                                count_array[j][k] = count_array[j][k] + count_date_event_array[i].count
                            }
                        }
                    }
                }
            };
            label_array=["Event"];
            for (var i=0;i<events_array.length;i++){
                label_array.push(events_array[i])
            };
            rows_for_draw[0]=label_array;
            console.log(rows_for_draw);
            console.log(count_array);
            for ( var i =0; i<date_array.length; i++){
                var draw_elem = [];
                draw_elem.push(date_array[i]);
                for (var j=0; j< events_array.length;j++){
                    var number = count_array[i][j];
                    draw_elem.push(number);
                }

                rows_for_draw.push(draw_elem);
            }
            console.log(rows_for_draw);
      var data = google.visualization.arrayToDataTable(rows_for_draw);

      var options =
        {title:"Количество событий за промежуток времени",
            width:1000, height:800,
            vAxis: {title: "Количество"}, isStacked: true,
            hAxis: {title: "Даты"}};
      var chart = new google.visualization.ColumnChart(document.getElementById("myChart"));
      chart.draw(data, options);
  }

        drawChart();
    };
    var eventUrl ="";
    events.forEach(function (newEvent) {
        eventUrl += "&event=" + newEvent
    })
    if (date_from != null && date_to != null)
        xmlhttp.open("get", "/get?date_from=" + date_from + "&date_to=" + date_to + eventUrl, true);
    else
        xmlhttp.open("get", "/get?event=" + event, true);
    xmlhttp.send();

}

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