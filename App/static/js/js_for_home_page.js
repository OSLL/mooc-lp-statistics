$(document).ready(function () {
    google.charts.load("current", {packages:['bar']});
    setFieldsAndClick();
    /* К тегу body привязывается функция, которая мониторит нажатие клавиши (keydown) во всех полях input на странице.
     И если происходит нажатие вызывает функцию function(e). Далее проверка - это enter или нет (e.keyCode === 13) и клик
     по баттону. Следущая строчка смена фокуса, чтобы мигающий курсив ниже переместился
     ( $(e.target).parent().next().find('.get-input-from-fields').focus();)*/
    $('body').delegate("input", "keydown", function(e) {
        if (e.keyCode === 13) {
            $('.btn-add').click();
            $(e.target).parent().next().find('.get-input-from-fields').focus();
        }
    });

});
$(function () {
    $('#first_date').datetimepicker({
        format: "YYYY-M-D H:M:S.mS"
    });
});
$(function () {
    $('#second_date').datetimepicker({
        format: "YYYY-M-D H:M:S.mS"
    });
});

function setFieldsAndClick() {
    var full_url = window.location.href;
    var uri = new URI(full_url);
    console.log(uri.search());

    var result = URI.parseQuery(uri.search());

    if (result["date_from"]) {
        document.getElementById('first_date').value = result["date_from"];
    }

    if (result["date_to"]) {
        document.getElementById('second_date').value = result["date_to"];
    }

    var events = result["event"];

    if (events) {
        if (events instanceof Array) {
            for (var i = 1; i < events.length; i++) {
                $('.glyphicon-plus').click();
            }

            for (var i = 0; i < events.length; i++) {
                document.getElementsByName('fields[]')[i].value = events[i];
            }

        } else {
            document.getElementsByName('fields[]')[0].value = events;
        }
    }

    var interval = result["selected_interval"];

    if (interval) {
        var set_intervals = document.getElementById('selected_interval')
        for (var i = 0; i < set_intervals.options.length; i++ ) {
            if (set_intervals.options[i].value == interval) {
                set_intervals.options[i].selected = "true";
            }
        }
    }

    if (result["date_from"] && result["date_to"] && events && interval) {
        document.getElementById('show-res').click();
    }
}

function fields_validation(elem) {
    $('#popup-filter').hide();
    var validation = true;
    var date_filter = elem[0];
    if (date_filter == null) {
        validation = false;
    }
    var params = elem[1];
    for (i = 0; i < params.length; i++) {
        if (params[i].length == 0) {
           validation = false;
        }
    }
    return validation;
}

function getUrlParams(data_from_filter) {
    if (data_from_filter[0] != null) {
        var date_from = data_from_filter[0][0];
        var date_to = data_from_filter[0][1]
    }
    var events = [];
    if (data_from_filter[1] != null) {
        data_from_filter[1].forEach(function (item) {
            events.push(item);
        })
    }
    var selected_interval = data_from_filter[2];
    var eventUrl ="";
    events.forEach(function (newEvent) {
        eventUrl += "&event=" + newEvent
    });
    var params;
    if (date_from != null && date_to != null) {
        params = 'date_from=' + date_from + '&date_to=' + date_to + eventUrl + '&selected_interval=' + selected_interval;
    } else {
        params = 'event=' + event;
    }
    return params;
}

function showSpin() {
    var opts = {
          lines: 12             // The number of lines to draw
        , length: 7             // The length of each line
        , width: 4              // The line thickness
        , radius: 10            // The radius of the inner circle
        , scale: 1.0            // Scales overall size of the spinner
        , corners: 1            // Roundness (0..1)
        , color: '#a2a2a2'         // #rgb or #rrggbb
        , opacity: 1/4          // Opacity of the lines
        , rotate: 0             // Rotation offset
        , direction: 1          // 1: clockwise, -1: counterclockwise
        , speed: 1              // Rounds per second
        , trail: 100            // Afterglow percentage
        , fps: 20               // Frames per second when using setTimeout()
        , zIndex: 2e9           // Use a high z-index by default
        , className: 'spinner'  // CSS class to assign to the element
        , top: '50%'            // center vertically
        , left: '50%'           // center horizontally
        , shadow: false         // Whether to render a shadow
        , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
        , position: 'absolute'  // Element positioning
    };
    var target = document.getElementById('myChart');
    var spinner = new Spinner(opts).spin(target)
}

function updateUrl(params) {
    window.history.pushState(null, null, '?' + params);
}

function processingData() {
    var data_from_filter = getData();
    if (fields_validation(data_from_filter) == false) {
        $('#popup-filter').show();
        return;
    }
    var params = getUrlParams(data_from_filter);
    var newRequestUrl = "/get?" + params;
    updateUrl(params);
    showSpin();

    $.get(newRequestUrl, function (html) {
        getListOfLogs(html);
        getGraphStat(html);
    });
}

function parseServerResponse(html) {
    var response = JSON.parse(html);
    var parsed_list = JSON.parse(response['a']);
    var parsed_stat = JSON.parse(response['b']);
    return [parsed_list, parsed_stat]
}

function getListOfLogs(html) {
    var row = '';
    var parsed_list = parseServerResponse(html)[0];
    for (var i in parsed_list) {
        var _date_time = parsed_list[i].Time.$date;
        var _UID = parsed_list[i].UID;
        var _event = parsed_list[i].Event;
        var _oid = parsed_list[i]['_id']['$oid'];
        row += '<a target="_blank" href="/get_log_entry/?id=' + _oid  + ' " class="list-group-item">' + '[' + _date_time + ']' + ' ' + '[' + _UID + ']' + ' ' + '[' + _event + ']' + '<br>';
    }
    document.getElementById("list-group").innerHTML = row;
}

function dataForGettingTable(parsed_stat) {
    var events_array = [];
    var date_array = [];
    var count_date_event_array = [];
    parsed_stat.forEach(function (elem) {
        events_array.push(elem.Event);
        var event_results_array = elem.Result;
        var date_str = '';
         for (var i in event_results_array) {
            if ('hour' in event_results_array[i]['_id']) {
                date_str = event_results_array[i]._id.hour + ':~:~ ' + event_results_array[i]._id.day + '.' + event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
            } else if ('day' in event_results_array[i]['_id']) {
                date_str = event_results_array[i]._id.day + '.' + event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
            } else if ('month' in event_results_array[i]['_id']) {
                date_str = event_results_array[i]._id.month + '.' + event_results_array[i]._id.year.toString().slice(-2);
            } else if ('year' in event_results_array[i]['_id']) {
                date_str = event_results_array[i]._id.year.toString();
            }
            date_array.push(date_str);
            count_date_event_array.push({
                "count": event_results_array[i].count,
                "date": date_str,
                "event": elem.Event
            });
        }
    });
    function uniqueVal(value, index, self) {
        return self.indexOf(value) === index;
    }
    date_array = date_array.filter(uniqueVal);
    console.log('date_array = ', date_array);
    console.log('count_date_event_array = ', count_date_event_array);
    console.log('events_array = ', events_array);
    return [date_array,count_date_event_array, events_array];
}

function createTableForColumnChart(parsed_stat) {
    var dataForFillingTable = dataForGettingTable(parsed_stat);
    var date_array = dataForFillingTable[0];
    var count_date_event_array = dataForFillingTable[1];
    var events_array = dataForFillingTable[2];
    var count_array = [];
    for (var i = 0; i < date_array.length; i++) {
        count_array.push([]);
        for (var j = 0; j < events_array.length; j++) {
            count_array[i].push(0);
        }
    }
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
    }
    var label_array =["Event"];
    for (var i = 0;i<events_array.length;i++){
        label_array.push(events_array[i])
    }
    var rows_for_draw = [0];
    rows_for_draw[0]=label_array;
    for ( var i = 0; i < date_array.length; i++){
        var draw_elem = [];
        draw_elem.push(date_array[i]);
        for (var j = 0; j< events_array.length;j++){
            var number = count_array[i][j];
            draw_elem.push(number);
        }

        rows_for_draw.push(draw_elem);
    }
    //       console.log(rows_for_draw);
    return rows_for_draw;
}

function drawColumnChart(parsed_stat) {
    var data = google.visualization.arrayToDataTable(createTableForColumnChart(parsed_stat));
    var options = {
        chart: {
            title:"Количество событий за промежуток времени"
        },
        bars: 'vertical',
        width:600, height:600,
        vAxis: {title: "Количество"},
        hAxis: {title: "Датa"}};
    var chart = new google.charts.Bar(document.getElementById("myChart"));
    chart.draw(data, google.charts.Bar.convertOptions(options));
}

function getGraphStat(html) {
    var parsed_stat = parseServerResponse(html)[1];
    drawColumnChart(parsed_stat);
}

function getData() {
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
    var selected_interval = document.getElementById("selected_interval").value;
    return [date_array, end_array, selected_interval];
}
function showSpinBDUpdate() {
    var opts = {
          lines: 12             // The number of lines to draw
        , length: 7             // The length of each line
        , width: 4              // The line thickness
        , radius: 10           // The radius of the inner circle
        , scale: 1.0            // Scales overall size of the spinner
        , corners: 1            // Roundness (0..1)
        , color: '#a2a2a2'         // #rgb or #rrggbb
        , opacity: 1/4          // Opacity of the lines
        , rotate: 0             // Rotation offset
        , direction: 1          // 1: clockwise, -1: counterclockwise
        , speed: 1              // Rounds per second
        , trail: 100            // Afterglow percentage
        , fps: 20               // Frames per second when using setTimeout()
        , zIndex: 2e9           // Use a high z-index by default
        , className: 'spinner'  // CSS class to assign to the element
        , top: '50%'            // center vertically
        , left: '50%'           // center horizontally
        , shadow: false         // Whether to render a shadow
        , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
        , position: 'absolute'  // Element positioning
    }
    var target = document.getElementById('update_date')
    var spinner = new Spinner(opts).spin(target)
}

function updateDB() {
    var requestUrl = "/update_log_in_db/";

    showSpinBDUpdate();

    $.get(requestUrl, function(html) {
        parseUpdateDBResult(html);
    });
}

function parseUpdateDBResult(html) {
    var target = document.getElementById('update_date');
    var response = JSON.parse(html);
    target.innerHTML = response['update_time'];
}