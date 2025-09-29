var map = L.map('map').setView([20.5937, 78.9629], 5);

// Adding satellite base layer as default
var satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; <a href="https://www.esri.com/">Esri</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);




// Adding single marker at centre of map
// var singleMArker = L.marker([20.8570, 73.9389])
//     .bindPopup('A pretty CSS popup.<br> Easily customizable.')
//     .openPopup();

// Add map scale
L.control.scale().addTo(map)

// map coordinate
map.on('mousemove', function (e) {
    document.querySelector('.coordinate').innerHTML = `Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`
})

// Markers and Clusters
// var marker = L.markerClusterGroup();
// // Assuming 'pins' comes from a file like test.js
// var taji = L.geoJson(pins, {
//     onEachFeature: function (feature, layer) {
//         layer.bindPopup('Test Popup');
//     }
// });
// taji.addTo(marker);
// marker.addTo(map);

// Leaflet layer control Objects (DO NOT CREATE THE CONTROL HERE)
var baseMaps = {
    '🛰️ Satellite': satellite
}

var overlayMaps = {
    // All overlay maps removed as requested
}

// L.control.layers(baseMaps, overlayMaps, {collapsed : false, position:'topleft'}).addTo(map); // <-- REMOVE THIS LINE