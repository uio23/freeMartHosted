// Close any pop-ups in 2 second
window.setTimeout(
  function() {
  $('.alert').alert('close');
  },
  2000
)

// Inform user if their product price is enough for bonus eligibility
function priceFeedback(minForBonus) {
  $('#productPrice').on('input', function() {
    input = $(this).val();
    if ((input < minForBonus) && ($.isNumeric(input))) {
      if (!($('.has-validation div').hasClass('bonus-feedback'))) {
        $(this).parent().append(`<div class="invalid-feedback bonus-feedback d-block">${minForBonus} FMC min for bonus</div>`);
      }
    } else {
      if ($('.has-validation div').hasClass('bonus-feedback')) {
        $('.bonus-feedback').remove();
      }
    }
  });
}
