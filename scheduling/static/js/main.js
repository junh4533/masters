$(document).ready(function () {

  $('#datetimepicker').datetimepicker({
    daysOfWeekDisabled: [0, 6],
    inline: true,
    sideBySide: true,
    format: 'YYYY-MM-DD',
    minDate: new Date().setHours(0, 0, 0, 0)
  });

  $("#datetimepicker").on("dp.change", function() {
    $('#datepicker').submit();
  });

  $('.toast').toast({
    delay: 10000
  });
  $('.toast').toast('show');

});

