$(document).ready(function () {

    $('#datetimepicker12').datetimepicker({
      inline: true,
      sideBySide: true,
      format: 'YYYY-MM-DD'
    });

    $("#datetimepicker12").on("dp.change", function(e) {
        $('#datepicker').submit();
    });

    // $("#login").modal({"backdrop": "static"});
});