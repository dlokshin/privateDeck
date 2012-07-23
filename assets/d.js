$(document).ready(function () {
    var sendData = 'city=' + geoip_city() + '&country=' + geoip_country_name() + '&state=' + geoip_region_name()
                    + '&name=' + userName + '&email=' + userEmail;

    var url = 'http://localhost:8080/log';

    $.post(url, sendData);
});
