/* darkMode functions definition */
function getCookie(cname) {
  var mode = document.cookie;
  var modeValue = mode.split('=')[1];
  return modeValue;
}


function switchToDarkMode() {
  $('html').attr('data-bs-theme', 'dark');

  /* Pass on the darkMode setting */
  document.cookie = "theme=dark; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/;"
}


function switchToLightMode() {
  $('html').removeAttr('data-bs-theme');

  /* Remove darkMode requirement for next page */
  document.cookie =  "theme=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
}


function switchDarkMode() {
  if ($('html').attr('data-bs-theme') == 'dark') {
    switchToLightMode();
  } else {
    switchToDarkMode();
  }
}


/* darkMode switching logic */
if (getCookie("theme") == "dark") {
  switchToDarkMode();
} else {
  switchToLightMode();
}
