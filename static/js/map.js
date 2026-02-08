document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([46.603354, 1.888334], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    if (typeof hospitalsData === 'undefined' || hospitalsData.length === 0) {
        return;
    }

    var bounds = [];

    hospitalsData.forEach(function (h) {
        var color = h.available ? 'green' : 'red';
        var icon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-' + color + '.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        var statusText = h.available ? 'Services disponibles' : 'Aucun service disponible';
        var statusClass = h.available ? 'text-success' : 'text-danger';

        var marker = L.marker([h.lat, h.lng], { icon: icon }).addTo(map);
        marker.bindPopup(
            '<strong>' + h.name + '</strong><br>' +
            h.city + '<br>' +
            '<span class="' + statusClass + '">' + statusText + '</span><br>' +
            '<a href="/hospital/' + h.id + '/">Voir détails</a>'
        );

        bounds.push([h.lat, h.lng]);
    });

    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [30, 30] });
    }
});
