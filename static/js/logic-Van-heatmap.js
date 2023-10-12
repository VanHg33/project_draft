console.log("logic-Van-heatmap.js")

// Build base map
// Use https://leaflet-extras.github.io/leaflet-providers/preview/
// basemap is Esri.WorldGrayCanvas
let basemap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    maxZoom: 16
});

// geomap is Esri.NatGeoWorldMap
var geomap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC',
    maxZoom: 16
});

let myMap = L.map("map", {
    center: [
        -27, 133
    ],
    zoom: 3
});

geomap.addTo(myMap);

// Build the menu
let baseMaps = {
    "Data Jobs Heatmap": basemap,
    "Australia Map": geomap
};

// Get Labels on Aus Map with Stadia.StamenTerrainLabels
let mapLabels = new L.LayerGroup();
let heatmap = new L.LayerGroup();

let overlays = {
    "Map Labels": mapLabels,
    "Australia Data Jobs OutLook": heatmap
};

L
    .control
    .layers(baseMaps, overlays, { collapsed: false })
    .addTo(myMap);



d3.json("http://127.0.0.1:5000/api/mapping", function (error, data) {
    if (error) return console.error(error);

    var jobData = [];
    data.forEach(function (d) {
        jobData.push({
            company: d["Employer name"],
            city: d["Job city"],
            title: d["Job title"],
            apply_link: d["Job apply link"],
            lat: d["Job latitude"],
            lng: d["Job longitude"]
        });
    });

    // Create the Leaflet map
    var map = L.map("map").setView([-27, 133], 5);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);

    // Add markers to the map
    jobData.forEach(function (d) {
        var marker = L.marker([d.lat, d.lng]).addTo(map);
        marker.bindPopup(`Company: ${d.company}<br>
                             City: ${d.city}<br>
                             Job Title: ${d.title}<br>
                             Remote: ${d.remote}<br>
                             Apply Link: <a href="${d.apply_link}">${d.apply_link}</a>`);
    });
});