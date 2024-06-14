$(document).ready(function() {
    $('.btn-check').change(function() {
        if ($('.btn-check:checked').length > 0){
            $('#btn-selecciondas').prop('disabled', false);
        } else {
            $('#btn-selecciondas').prop('disabled', true);
        }
    });
  });

