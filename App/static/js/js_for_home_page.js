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
        return [date_array, end_array];

    }
    else {
        alert("Неправильный формат даты");
        return null;
    }
}