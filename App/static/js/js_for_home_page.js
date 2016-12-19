function write_list() {;
    elem = getdate();
    if (elem[0] != null) {
        var date_from = elem[0][0];
        var date_to = elem[0][1]
    }
    if (elem[1] != null) {
        var event = elem[1][0]
    }
    var xmlhttp = null;
    var date_array = [];
    var count_array = [];
    var rows_for_draw = [];
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
            console.log(parsed_stat);
            var date_str = ''
            for (var i in parsed_stat) {
                if ('hour' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.hour + ':~:~ ' + parsed_stat[i]._id.day + '.' + parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                    count_array.push(parsed_stat[i].count);
                    date_array.push(date_str);
                } else if ('day' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.day + '.' + parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                    count_array.push(parsed_stat[i].count);
                    date_array.push(date_str);
                } else if ('month' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.month + '.' + parsed_stat[i]._id.year.toString().slice(-2);
                    count_array.push(parsed_stat[i].count);
                    date_array.push(date_str);
                } else if ('year' in parsed_stat[i]['_id']) {
                    date_str = parsed_stat[i]._id.year.toString().slice(-2);
                    count_array.push(parsed_stat[i].count);
                    date_array.push(date_str);
                }
            }
            for (var i in parsed_list) {
                row += '<a href="#" class="list-group-item">' + '[' + parsed_list[i].Time.$date + ']' + ' ' + '[' + parsed_list[i].UID + ']' + ' ' + '[' + parsed_list[i].Event + ']' + '<br>';
            }
            document.getElementById("list-group").innerHTML = row;

        }
        function drawStuff() {
            var data = new google.visualization.DataTable();
            data.addColumn('string','День');
            data.addColumn('number');

            for (var i = 0; i < date_array.length; i++) {
                rows_for_draw.push([date_array[i], count_array[i]]);
            }
            data.addRows(rows_for_draw);
            var options = {
                title: 'Chess opening moves',
                legend: {position: 'center'},
                chart: {
                    title: 'Количество событий за промежуток времени',
                },
                bars: 'vertical', // Required for Material Bar Charts.
                axes: {
                    x: {
                        0: {side: 'bottom', label: 'Время'} // Top x-axis.
                    },
                    y: {
                        0: {side: 'left', label: 'Количество событий'} // Top x-axis.
                    }

                },
                bar: {groupWidth: "90%"},
                width: 700,
                height: 540,
                isStacked: true
            };

            var chart = new google.charts.Bar(document.getElementById('myChart'));
            chart.draw(data, options);
        };
        drawStuff();
    };

    if (date_from != null && date_to != null)
        xmlhttp.open("get", "/get?date_from=" + date_from + "&date_to=" + date_to + "&event=" + event, true);
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