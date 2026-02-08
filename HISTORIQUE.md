# Historique du projet Urgencio

## 2026-02-08

### 1. Création du projet Django
- Installation de Django 6.0.2 dans le venv `/opt/workspace/urgence/venv/`
- Création du projet `urgencio` et de l'app `hospitals`
- Création de la structure de dossiers (templates, static)
- Fichier `requirements.txt` créé

### 2. Modèles de données
- **Hospital** : name, address, city, phone, latitude, longitude, user (OneToOne)
- **Service** : hospital (FK), name, is_available, queue_count, estimated_wait_time, last_updated
- Migration initiale `0001_initial.py` générée et appliquée

### 3. Configuration Django
- `settings.py` : ajout de l'app `hospitals`, langue `fr-fr`, timezone `Europe/Paris`, `ALLOWED_HOSTS = ['*']`, `STATICFILES_DIRS`
- `urls.py` projet : inclusion des URLs de `hospitals`

### 4. Backend (views, URLs, forms, admin)
- **Views** : home, hospital_list (filtre ville + recherche), hospital_detail, login_view, logout_view, dashboard (formset)
- **URLs** : `/`, `/hospitals/`, `/hospital/<id>/`, `/login/`, `/logout/`, `/dashboard/`
- **Forms** : `ServiceUpdateForm` (ModelForm pour mettre à jour disponibilité, queue, temps d'attente)
- **Admin** : `HospitalAdmin` avec `ServiceInline`, `ServiceAdmin` avec filtres et recherche

### 5. Frontend (templates + static)
- **base.html** : navbar Bootstrap 5, messages, footer, chargement Leaflet.js
- **home.html** : carte Leaflet + aperçu des hôpitaux en cards
- **hospital_list.html** : liste filtrable par ville + recherche
- **hospital_detail.html** : tableau des services avec disponibilité, queue, temps d'attente
- **dashboard.html** : formulaire de mise à jour des services (staff hôpital)
- **login.html** : page de connexion
- **style.css** : effets hover sur les cards, layout flexbox
- **map.js** : carte Leaflet avec marqueurs vert/rouge selon disponibilité

### 6. Données de test
- Superuser : `admin` / `admin123`
- 3 hôpitaux avec comptes :
  - `hopital_paris` / `hospital123` → Hôpital Saint-Antoine (Paris)
  - `hopital_lyon` / `hospital123` → Hôpital Édouard Herriot (Lyon)
  - `hopital_marseille` / `hospital123` → Hôpital de la Timone (Marseille)
- 9 services au total (Urgences, Cardiologie, Pédiatrie, Traumatologie, Neurologie)

### 7. Installation de Node.js et @openai/codex
- Installation de Node.js v24.13.0 via nvm
- Installation globale de `@openai/codex` v0.98.0

### 8. Lancement du serveur
- Serveur Django lancé sur `0.0.0.0:8000`

### 9. Recentrage sur les urgences à Paris uniquement
- **Modèle Hospital** : remplacement du champ `city` par `arrondissement` (choix 1e-20e)
- **Modèle Service** : ajout de `TYPE_CHOICES` avec 9 types d'urgences spécialisées :
  - Urgences générales, pédiatriques, cardiologiques, psychiatriques, ophtalmologiques, dentaires, gynéco/obstétriques, ORL, main & traumatologie
- **Views** : filtres par arrondissement + type d'urgence (remplace filtre par ville)
- **Templates** : tous mis à jour pour afficher "Paris Xe" au lieu de la ville
- **Carte** : centrée sur Paris (zoom 12) au lieu de toute la France
- **Données** : 12 vrais hôpitaux AP-HP parisiens avec 37 services d'urgence :
  - Pitié-Salpêtrière (13e), Hôtel-Dieu (4e), Saint-Antoine (12e), Lariboisière (10e), Saint-Louis (10e), Tenon (20e), Cochin (14e), Necker (15e), HEGP (15e), Bichat (18e), Robert-Debré (19e), Trousseau (12e)
- Comptes hôpitaux : tous avec mot de passe `hospital123`

### 10. Hôpitaux les plus proches (API Opendatasoft + Géolocalisation)
- **`hospitals/utils.py`** : fonction Haversine pour calculer la distance en km entre deux points GPS
- **`hospitals/views.py`** : vue `nearest_hospitals` — endpoint JSON `/api/nearest/?lat=...&lon=...&limit=...`
  - Interroge en live l'API Opendatasoft (dataset FINESS Île-de-France, filtre Paris dept 75)
  - Trie les résultats par distance via Haversine
  - Renvoie les N hôpitaux les plus proches
- **`hospitals/urls.py`** : route `/api/nearest/`
- **`static/js/nearest.js`** : géolocalisation HTML5 du navigateur + appel à l'endpoint + rendu des cards
  - Fallback : si géolocalisation refusée, affiche depuis le centre de Paris (48.8566, 2.3522)
- **`home.html`** : nouveau bloc "Hôpitaux les plus proches de vous" entre la carte et la liste Urgencio
- **`hospitals/tests.py`** : 6 tests unitaires (Haversine : même point, Paris→Lyon, courte distance, symétrie + API : params manquants, params invalides)
- Source de données : API `data.iledefrance.fr` dataset `les_etablissements_hospitaliers_franciliens`

### 11. Géolocalisation utilisateur visible sur la carte
- **Bouton "Me localiser"** (&#9737;) ajouté en haut à gauche de la carte Leaflet
- **Marqueur bleu pulsant** affiche la position de l'utilisateur sur la carte
- **Cercle de précision** bleu semi-transparent autour de la position
- **Recentrage automatique** de la carte sur la position de l'utilisateur
- **Géolocalisation automatique** au chargement de la page + possibilité de relancer via le bouton
- **Coordination map.js ↔ nearest.js** : la géolocalisation est centralisée dans map.js qui déclenche la recherche des hôpitaux proches via nearest.js
- **Fallback** : si géolocalisation refusée → centre de Paris + message d'avertissement
- **CSS** : animation pulse pour le marqueur utilisateur (`style.css`)

### 12. Cohérence carte ↔ liste des hôpitaux proches
- **Marqueurs violets** sur la carte pour les hôpitaux FINESS proches (en plus des vert/rouge Urgencio)
- `nearest.js` appelle `urgencioMap.addNearestMarkers()` quand les résultats API arrivent
- `map.js` expose `addNearestMarkers()` qui ajoute/remplace les marqueurs violets
- **Légende** ajoutée en bas à droite de la carte : vert (disponible), rouge (indisponible), violet (FINESS proche), bleu (votre position)
- Les popups des marqueurs violets affichent : nom, adresse, ville, téléphone, catégorie, distance

### 13. Nettoyage — tout sur l'API FINESS, suppression affichage DB locale
- **home.html** : supprimé le bloc "Hôpitaux parisiens (Urgencio)" (cards de la DB locale)
- **views.py** : `home()` nettoyé, ne passe plus `hospitals` ni `hospitals_json` au template
- **map.js** : supprimé les marqueurs vert/rouge de la DB locale, garde uniquement position utilisateur (bleu) + hôpitaux FINESS (violet)
- **Légende** simplifiée : violet (hôpital proche) + bleu (votre position)
- **nearest.js** : charge 50 résultats, stocke tout en mémoire, filtre côté front
- **Filtre par catégorie** (dropdown) : rempli dynamiquement avec les catégories FINESS + compteurs, filtre les cards ET les marqueurs carte en temps réel
- **Scroll area** : liste des hôpitaux dans une zone scrollable (`scroll-area` CSS)
