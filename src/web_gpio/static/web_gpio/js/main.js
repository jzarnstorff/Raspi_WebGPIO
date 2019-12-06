$(document).ready(function(){
  $.ajax({
    type: 'GET',
    url: 'rpi_gpio/api/',
    success: function(pins) {
      $.each(pins, function(index, pin) {
        if (pin.state) {
          $('[data-buttonID=' + pin.id + ']').find('img').toggle();
        }
      });
    }
  });

  $('.image-button').on('click', function(){
    var btnID = $(this).attr('data-buttonID');
    $(this).find('img').toggle();
    $.get('/rpi_gpio/', {button_id: btnID}, function(data){
    });
  });
});
