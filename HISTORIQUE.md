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
