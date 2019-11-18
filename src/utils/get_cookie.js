function getCookie(name) {
    /* This function returns the cookie for request
     * Attach it to the HTTP request to identify the user
     * using session authentication instead of token authentication
     */

     var cookieValue = null;

     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i=0; i<cookies.length; i++) {
             var cookie = jQuery.trim(cookies[0]);

             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(
                     cookie.substring(name.length + 1)
                 );
                 break;
             }
         }
     }

     return cookieValue;
}
