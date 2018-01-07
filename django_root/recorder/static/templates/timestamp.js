$(document).ready(function () {
    const dateSelector = $('.date-picker').datetimepicker({
        inline: true,
        format: 'yyyy-MM-dd'
    });

    const timeSelector = $('.start-time-picker').datetimepicker({
        inline: true,
        format: 'HH:mm',
        defaultDate: moment().hour(0).minute(0)
    });

    $('#submit-button').click(function (event, data) {
        const employeeId = $(this).attr("data-employee-id");
        const groupId = $(this).attr("data-group-id");
        const machineId = $(this).attr("data-machine-id");
        const dateSelected = dateSelector.data('DateTimePicker').date();
        const time = timeSelector.data('DateTimePicker').date();
        const totalMinutes = time.hour() * 60 + time.minute();
        const commentId = $('#comment-selector').val();
        if (totalMinutes > 0) {
            $.post(window.location.pathname, {
                employee_id: employeeId,
                machine_id: machineId,
                date: dateSelected.format('YYYY-MM-DD'),
                duration: totalMinutes,
                comment_id: commentId
            }, function (data, status) {
                if (status === 'success') {
                    window.location.href = '/groups/' + groupId;
                } else {
                    alert('Oops, something went wrong...')
                }
            });
        }
    });
});