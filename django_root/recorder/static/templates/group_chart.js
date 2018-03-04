var initChart = function (ctx) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: null,
            datasets: [{
                label: 'Stunden',
                data: null,
                backgroundColor: '#00759F',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: false
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
};

var reduceDate = function (data) {
    var startDate = $('#start-date-input').val();
    var endDate = $('#end-date-input').val();

    return _.reduce(data, function (memo, entry) {
        var entryDate = moment(entry.date);
        var employeeId = entry.employee.id;
        var match = _.find(memo, function (item) { return item.employee.id === employeeId });
        if (!match) {
            match = {employee: entry.employee, duration: 0};
            memo.push(match);
        }
        if (entryDate.isBetween(startDate, endDate, 'day', '[]')) {
            match.duration += entry.duration;
        }
        return memo;
    }, []);
};

var reloadChart = function (chart) {
    var groupId = window.location.pathname.split('/')[2];
    $.get('/api/groups/' + groupId, function (data) {
        var chartData = reduceDate(data);
        chart.data.labels = _.map(chartData, function (entry) { return entry.employee.first_name + ' ' + entry.employee.last_name })
        chart.data.datasets[0].data = _.map(chartData, function (entry) { return parseInt(entry.duration / 60) });
        chart.update()
    });
};

$(document).ready(function () {
    var ctx = document.getElementById("myChart").getContext('2d');
    var chart = initChart(ctx);

    var weekStart = moment().startOf('week').add(1, 'day');
    var weekEnd = moment().endOf('week').subtract(1, 'day');

    $('#start-date-input').val(weekStart.format('YYYY-MM-DD'));
    $('#end-date-input').val(weekEnd.format('YYYY-MM-DD'));

    $('.form-control').change(function () {
        reloadChart(chart);
    });

    reloadChart(chart);
});