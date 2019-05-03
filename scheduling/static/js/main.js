$(document).ready(function () {

  $('#datetimepicker').datetimepicker({
    daysOfWeekDisabled: [0, 6],
    inline: true,
    sideBySide: true,
    format: 'YYYY-MM-DD',
    minDate: new Date().setHours(0, 0, 0, 0)
  });

  $("#datetimepicker").on("dp.change", function (e) {
    // date = $('#datetimepicker').serialize().replace('date=', '');
    date = $('#date').val();
    console.log(date);

    $.ajax({
      type: 'GET',
      url: '../make_appointments/',
      data: {
        date: date
      },
      success: function(){
        $("#available").html(date);  
        $("#submit_date").val(date);  
      }
    });
  });

  function confirm_delete(){
    var delete_appointment = confirm("continue?");
    if(delete_appointment == true){
      $('#delete').submit();
    }
  }

  

  // $("#datetimepicker").on("dp.change", function (e) {
  //   $('#datepicker').submit();
  // });

  // $(document).on("submit","#datepicker",function(e){ 
  //   e.preventDefault();
  //     // e.stopImmediatePropagation();
  //   // date = $('#datepicker').serialize().replace('date=', '');
  //   console.log(date);

  //   $.ajax({
  //     type: 'GET',
  //     url: '../make_appointments/',
  //     data: {
  //       // 'date': date
  //       date: $('#date').val()
  //     },
  //     success: function(){
        
  //     }
  //   });
  // });



});

