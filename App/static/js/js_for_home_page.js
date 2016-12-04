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
