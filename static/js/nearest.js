document.addEventListener('DOMContentLoaded', function () {
    var statusEl = document.getElementById('nearest-status');
    var cardsEl = document.getElementById('nearest-cards');
    var filterEl = document.getElementById('filter-category');

    if (!statusEl || !cardsEl) return;

    var allHospitals = [];

    window.urgencioNearest = {
        fetchNearest: fetchNearest
    };

    // Filtre par catégorie
    if (filterEl) {
        filterEl.addEventListener('change', function () {
            applyFilter(this.value);
        });
    }

    function fetchNearest(lat, lon) {
        statusEl.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Recherche des hôpitaux proches...';

        fetch('/api/nearest/?lat=' + lat + '&lon=' + lon + '&limit=50')
            .then(function (resp) {
                if (!resp.ok) throw new Error('Erreur serveur');
                return resp.json();
            })
            .then(function (data) {
                allHospitals = data.hospitals || [];
                if (allHospitals.length > 0) {
                    populateFilter(allHospitals);
                    applyFilter('');
                } else {
                    statusEl.textContent = 'Aucun hôpital trouvé à proximité.';
                }
            })
            .catch(function () {
                statusEl.innerHTML = '<span class="text-danger">Erreur lors de la recherche des hôpitaux proches.</span>';
            });
    }

    function populateFilter(hospitals) {
        if (!filterEl) return;
        var categories = {};
        hospitals.forEach(function (h) {
            if (h.category) categories[h.category] = true;
        });
        var sorted = Object.keys(categories).sort();
        filterEl.innerHTML = '<option value="">Tous les types (' + hospitals.length + ')</option>';
        sorted.forEach(function (cat) {
            var count = hospitals.filter(function (h) { return h.category === cat; }).length;
            var opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat + ' (' + count + ')';
            filterEl.appendChild(opt);
        });
    }

    function applyFilter(category) {
        var filtered = allHospitals;
        if (category) {
            filtered = allHospitals.filter(function (h) { return h.category === category; });
        }
        statusEl.textContent = filtered.length + ' hôpital(aux) trouvé(s) (source : FINESS / Île-de-France)';
        renderCards(filtered);
        if (window.urgencioMap && window.urgencioMap.addNearestMarkers) {
            window.urgencioMap.addNearestMarkers(filtered);
        }
    }

    function renderCards(hospitals) {
        var html = '';
        hospitals.forEach(function (h) {
            html += '<div class="col-md-6 col-lg-4 mb-3">' +
                '<div class="card hospital-card h-100 border-primary">' +
                '<div class="card-body">' +
                '<h6 class="card-title">' + escapeHtml(h.name) + '</h6>' +
                '<p class="card-text small">' +
                (h.address ? escapeHtml(h.address) + '<br>' : '') +
                escapeHtml(h.city) + '<br>' +
                (h.phone ? 'Tél : ' + escapeHtml(h.phone) + '<br>' : '') +
                '<span class="badge bg-info">' + escapeHtml(h.category) + '</span>' +
                '</p>' +
                '<span class="badge bg-dark">' + h.distance_km + ' km</span>' +
                '</div>' +
                '</div>' +
                '</div>';
        });
        cardsEl.innerHTML = html;
    }

    function escapeHtml(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
