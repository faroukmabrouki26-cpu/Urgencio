document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([48.8566, 2.3522], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // --- Bouton "Me localiser" ---
    var LocateControl = L.Control.extend({
        options: { position: 'topleft' },
        onAdd: function () {
            var btn = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            btn.innerHTML = '<a href="#" id="locate-btn" title="Me localiser" ' +
                'style="display:flex;align-items:center;justify-content:center;' +
                'width:34px;height:34px;font-size:20px;text-decoration:none;' +
                'background:#fff;cursor:pointer;">&#9737;</a>';
            L.DomEvent.disableClickPropagation(btn);
            return btn;
        }
    });
    map.addControl(new LocateControl());

    // --- Légende ---
    var LegendControl = L.Control.extend({
        options: { position: 'bottomright' },
        onAdd: function () {
            var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            div.style.cssText = 'background:#fff;padding:8px 12px;font-size:12px;line-height:1.8;';
            div.innerHTML =
                '<strong>Légende</strong><br>' +
                '<img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png" style="height:16px;vertical-align:middle;"> Hôpital proche<br>' +
                '<span style="display:inline-block;width:12px;height:12px;background:#4285F4;border-radius:50%;border:2px solid #fff;vertical-align:middle;"></span> Votre position';
            return div;
        }
    });
    map.addControl(new LegendControl());

    var userMarker = null;
    var userCircle = null;
    var nearestMarkers = [];

    document.getElementById('locate-btn').addEventListener('click', function (e) {
        e.preventDefault();
        locateUser();
    });

    // Exposer les fonctions pour nearest.js
    window.urgencioMap = {
        addNearestMarkers: addNearestMarkers
    };

    function locateUser() {
        var statusEl = document.getElementById('nearest-status');
        if (statusEl) {
            statusEl.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Recherche de votre position...';
        }

        if (!navigator.geolocation) {
            if (statusEl) statusEl.innerHTML = '<span class="text-warning">Géolocalisation non supportée par votre navigateur.</span>';
            return;
        }

        navigator.geolocation.getCurrentPosition(
            function (pos) {
                var lat = pos.coords.latitude;
                var lon = pos.coords.longitude;
                var accuracy = pos.coords.accuracy;
                showUserPosition(lat, lon, accuracy);
                if (window.urgencioNearest) {
                    window.urgencioNearest.fetchNearest(lat, lon);
                }
            },
            function () {
                if (statusEl) statusEl.innerHTML = '<span class="text-warning">Géolocalisation refusée — affichage depuis le centre de Paris.</span>';
                showUserPosition(48.8566, 2.3522, null);
                if (window.urgencioNearest) {
                    window.urgencioNearest.fetchNearest(48.8566, 2.3522);
                }
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );
    }

    function showUserPosition(lat, lon, accuracy) {
        if (userMarker) map.removeLayer(userMarker);
        if (userCircle) map.removeLayer(userCircle);

        var userIcon = L.divIcon({
            className: 'user-location-icon',
            html: '<div class="user-dot"></div><div class="user-pulse"></div>',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        userMarker = L.marker([lat, lon], { icon: userIcon, zIndexOffset: 1000 }).addTo(map);
        userMarker.bindPopup('<strong>Vous êtes ici</strong>').openPopup();

        if (accuracy && accuracy < 5000) {
            userCircle = L.circle([lat, lon], {
                radius: accuracy,
                color: '#4285F4',
                fillColor: '#4285F4',
                fillOpacity: 0.1,
                weight: 1
            }).addTo(map);
        }

        map.setView([lat, lon], 14);
    }

    function addNearestMarkers(hospitals) {
        nearestMarkers.forEach(function (m) { map.removeLayer(m); });
        nearestMarkers = [];

        var violetIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        hospitals.forEach(function (h) {
            var marker = L.marker([h.lat, h.lng], { icon: violetIcon }).addTo(map);
            marker.bindPopup(
                '<strong>' + h.name + '</strong><br>' +
                (h.address ? h.address + '<br>' : '') +
                h.city + '<br>' +
                (h.phone ? 'Tél : ' + h.phone + '<br>' : '') +
                '<em>' + h.category + '</em><br>' +
                '<span class="badge bg-dark">' + h.distance_km + ' km</span>'
            );
            nearestMarkers.push(marker);
        });
    }

    locateUser();
});
