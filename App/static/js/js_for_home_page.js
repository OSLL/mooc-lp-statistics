function fields_validation() {
    $('#popup-filter').hide();
    var elem = getdate();
    var validation = true;
    var date = elem[0];
    var params = elem[1];

    for (i = 0; i < params.length; i++) {
        if (params[i].length == 0) {
           validation = false;
        }
    }
    if (!date) {
        validation = false;
    }
    if (validation) {
        write_list();
    } else {
        $('#popup-filter').show();
    }
}

function write_list() {
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
            var date_str = '';
            parsed_stat.forEach(function (elem) {
                events_array.push(elem.Event);
            });
            function uniqueVal(value, index, self) {
                return self.indexOf(value) === index;
            }
            console.log('events_array = ', events_array);
            parsed_stat.forEach(function (elem) {
                var event_results_array = elem.Result;
                for (var i in event_results_array) {
                    if ('hour' in event_results_array[i]['_id']) {
                        date_str = event_results_array[i]._id.hour + ':~:~ ' + event_results_array[i]._id.day + '.' + event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
                    } else if ('day' in event_results_array[i]['_id']) {
                        date_str = event_results_array[i]._id.day + '.' + event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
                    } else if ('month' in parsed_stat[i]['_id']) {
                        date_str = event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
                    } else if ('year' in event_results_array[i]['_id']) {
                        date_str = event_results_array[i]._id.year.toString().slice(-2);
                    }
                    date_array.push(date_str);
                    count_date_event_array.push({
                        "count": event_results_array[i].count,
                        "date": date_str,
                        "event": elem.Event
                    });
                }
            });
            date_array = date_array.filter(uniqueVal).sort();
            console.log('date_array = ', date_array);
            console.log('count_date_event_array = ', count_date_event_array);

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
     //       console.log(rows_for_draw);
     //       console.log(count_array);
            for ( var i =0; i<date_array.length; i++){
                var draw_elem = [];
                draw_elem.push(date_array[i]);
                for (var j=0; j< events_array.length;j++){
                    var number = count_array[i][j];
                    draw_elem.push(number);
                }

                rows_for_draw.push(draw_elem);
            }
     //       console.log(rows_for_draw);
      var data = google.visualization.arrayToDataTable(rows_for_draw);

      var options =
        {title:"Количество событий за промежуток времени",
            width:900, height:600,
            vAxis: {title: "Количество"},
            hAxis: {title: "Даты"}};
      var chart = new google.charts.Bar(document.getElementById("myChart"));
      chart.draw(data, options);
  }

        drawChart();
    };
    var eventUrl ="";
    events.forEach(function (newEvent) {
        eventUrl += "&event=" + newEvent
    });
    var params;
    if (date_from != null && date_to != null) {
        params = 'date_from=' + date_from + '&date_to=' + date_to + eventUrl;
    } else {
        params = 'event=' + event;
    }
    console.log('get.request = ', "/get?" + params);
    xmlhttp.open('GET', "/get?" + params, true);
    xmlhttp.send();

}

function getdate() {
    var regexp;
    regexp = /(\d{4}\-\d{1,2})\-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}\.\d{1,6}/;
    var first_date = document.getElementById('first_date').value;
    var second_date = document.getElementById('second_date').value;
    var end_array = [];
    //var filters_array = $('input#filterArrayId.form-control');
    var filters_array = $('input.get-input-from-fields');

    for (i = 0; i < filters_array.length; i++) {
        end_array.push(filters_array[i].value);
    }
    for (i = 0; i < end_array.length; i++){
        console.log("input", i, "=",  end_array[i]);
    }
    console.log("end_array.length", end_array.length);

    if (regexp.test(first_date) && regexp.test(second_date)) {
        var date_array;
        date_array = [first_date, second_date];
    }

    return [date_array, end_array];
}