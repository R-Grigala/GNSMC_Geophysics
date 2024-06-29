var stations = [];

function initMap() {
    var latlng = new google.maps.LatLng(42.264, 43.322);
    var myOptions = {
        zoom: 7,
        center: latlng,
        panControl: false,
        streetViewControl: false,
        mapTypeControl: true,
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoomControl: true,
        zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL}
    };
    var map = new google.maps.Map(document.getElementById("map"), myOptions);
    fetchAndSetMarkers(map);
}

function fetchAndSetMarkers(map) {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            stations = data;
            // console.log(stations);
            setMarkers(map);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function setMarkers(map) {
    for (var i = 0; i < stations.length; i++) {
        var station = stations[i];
        var marker = new google.maps.Marker({
            position: {lat: parseFloat(station.tStLatitude), lng: parseFloat(station.tStLongitude)},
            map: map,
            title: station.tStCode
        });
        attachInfoWindow(marker, station);
    }
}

function attachInfoWindow(marker, station) {
    var infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="text-center">
                <strong>კოდი: ${station.tStCode}</strong><br>
                ქსელის კოდი: ${station.tStNetworkCode}<br>
                ადგილმდებარეობა: ${station.tStLocation}<br>
                განედი: ${station.tStLatitude}<br>
                გრძედი: ${station.tStLongitude}<br>
                სიმაღლე(მ): ${station.tStElevation}<br>
                გახსნის დღე: ${station.tStOpenDate}<br>
                დახურვის დღე: ${station.tStCloseDate}<br>
                ტიპი: ${station.tStType}<br>
            </div>`
    });
    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });
}

// Initialize the map when the page loads
document.addEventListener("DOMContentLoaded", function() {
    initMap();
});