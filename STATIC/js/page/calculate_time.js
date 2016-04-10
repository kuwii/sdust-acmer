function calculate_time() {
  $(".calculate-time").each(function() {
    var UnixTime = (parseInt($(this).text()) + 8 * 60 * 60) * 1000;
    var dateObj = new Date(UnixTime);
    var UnixTimeToDate = dateObj.getUTCFullYear() + '-' + (dateObj.getUTCMonth() +1 ) + '-' + dateObj.getUTCDate() + ' ' + dateObj.getUTCHours() + ':' + dateObj.getUTCMinutes() + ':' + dateObj.getUTCSeconds();
    $(this).text(UnixTimeToDate);
  });
}

$(document).ready(function() {
  calculate_time();
});