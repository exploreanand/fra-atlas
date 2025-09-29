// Full Screen
var mapId = document.getElementById('map');
function fullScreenView() {
    if(document.fullscreenElement){
        document.exitFullscreen()
    }
    else{
        mapId.requestFullscreen();
    }
}

L.control.browserPrint({position: 'topright'}).addTo(map);

// Search
new L.Control.Geocoder().addTo(map);

// Measure Function
L.control.measure({
    primaryLengthUnit: 'meters',
    secondaryLengthUnit: 'kilometers',
    primaryAreaUnit: 'sqmeters',
    secondaryAreaUnit: 'hectares',
    activeColor: '#ABE67E',
    completedColor: '#C8F2BE'
}).addTo(map);


// Zoom to layer
$('.zoom-to-layer').click(function () {
    map.setView([20.5937, 78.9629], 5)
})