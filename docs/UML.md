# Urgencio - Diagrammes UML

## 1. Diagramme de Classes

```
┌─────────────────────────┐       ┌─────────────────────────────┐
│      User (Django)      │       │          Hospital           │
│─────────────────────────│       │─────────────────────────────│
│ id : int                │       │ id : int                    │
│ username : str          │       │ name : str                  │
│ password : str          │       │ address : str               │
│ email : str             │       │ arrondissement : str (1-20) │
│ is_staff : bool         │       │ phone : str                 │
│─────────────────────────│       │ latitude : float            │
│ login()                 │       │ longitude : float           │
│ logout()                │       │ user : OneToOne(User)       │
└────────┬────────────────┘       │─────────────────────────────│
         │                        │ get_services()              │
         │ 1                      │ is_any_service_available()  │
         │                        │ __str__()                   │
         │          OneToOne      └────────────┬────────────────┘
         └─────────────────────────────────────┘
                                               │ 1
                                               │
                                               │ 1..*
                                               ▼
                                  ┌─────────────────────────────┐
                                  │          Service            │
                                  │─────────────────────────────│
                                  │ id : int                    │
                                  │ hospital : FK(Hospital)     │
                                  │ name : str (TYPE_CHOICES)   │
                                  │ is_available : bool         │
                                  │ queue_count : int           │
                                  │ estimated_wait_time : int   │
                                  │ last_updated : datetime     │
                                  │─────────────────────────────│
                                  │ update_queue(count, wait)   │
                                  │ toggle_availability()       │
                                  │ get_name_display()          │
                                  │ __str__()                   │
                                  └─────────────────────────────┘

TYPE_CHOICES :
  generales, pediatriques, cardiologiques, psychiatriques,
  ophtalmologiques, dentaires, gyneco_obstetrique, orl, main_traumato
```

**Relations :**
- `User` ←(1:1)→ `Hospital` : Chaque hôpital a un seul compte utilisateur
- `Hospital` ←(1:N)→ `Service` : Un hôpital a plusieurs services d'urgence

---

## 2. Diagramme de composants

```
┌──────────────────────────────────────────────────────────────────────┐
│                           URGENCIO                                   │
│                                                                      │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────────┐  │
│  │  Browser     │    │  Django      │    │  API Opendatasoft       │  │
│  │             │    │  Backend     │    │  (FINESS IDF)           │  │
│  │ ┌─────────┐ │    │ ┌──────────┐ │    │                         │  │
│  │ │ map.js  │─┼───>│ │ views.py │─┼───>│  data.iledefrance.fr    │  │
│  │ │         │ │    │ │          │ │    │  /les_etablissements_   │  │
│  │ │Leaflet  │ │    │ │nearest_  │ │    │  hospitaliers_          │  │
│  │ │+Geoloc  │ │    │ │hospitals │ │    │  franciliens            │  │
│  │ └─────────┘ │    │ └──────────┘ │    └─────────────────────────┘  │
│  │ ┌─────────┐ │    │ ┌──────────┐ │    ┌─────────────────────────┐  │
│  │ │nearest. │─┼───>│ │utils.py  │ │    │  SQLite (db.sqlite3)    │  │
│  │ │  js     │ │    │ │haversine │ │    │                         │  │
│  │ │         │ │    │ └──────────┘ │    │  Hospital, Service      │  │
│  │ │filtre   │ │    │ ┌──────────┐ │    │  (dashboard staff)      │  │
│  │ │catégorie│ │    │ │dashboard │─┼───>│                         │  │
│  │ └─────────┘ │    │ └──────────┘ │    └─────────────────────────┘  │
│  └─────────────┘    └──────────────┘                                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Diagramme de Cas d'Utilisation (Use Case)

```
┌─────────────────────────────────────────────────────────────────┐
│                        URGENCIO                                 │
│                                                                 │
│   ┌─────────────────────────────────────────────┐               │
│   │  Visiteur (Public)                          │               │
│   │                                             │               │
│   │  ○ Voir la carte des hôpitaux (Paris)       │               │
│   │  ○ Se géolocaliser sur la carte             │               │
│   │  ○ Voir les hôpitaux les plus proches       │               │
│   │  ○ Filtrer par catégorie d'établissement    │               │
│   │  ○ Rechercher un hôpital par nom            │               │
│   │  ○ Filtrer par arrondissement               │               │
│   │  ○ Voir le détail d'un hôpital              │               │
│   │  ○ Voir la disponibilité des services       │               │
│   │  ○ Voir le nombre de patients en queue      │               │
│   └─────────────────────────────────────────────┘               │
│                                                                 │
│   ┌─────────────────────────────────────────────┐               │
│   │  Staff Hôpital (Authentifié)                │               │
│   │                                             │               │
│   │  ○ Se connecter / Se déconnecter            │               │
│   │  ○ Accéder au dashboard                     │               │
│   │  ○ Mettre à jour la disponibilité           │               │
│   │  ○ Mettre à jour le nombre en queue         │               │
│   │  ○ Mettre à jour le temps d'attente         │               │
│   └─────────────────────────────────────────────┘               │
│                                                                 │
│   ┌─────────────────────────────────────────────┐               │
│   │  Admin Central                              │               │
│   │                                             │               │
│   │  ○ Gérer les hôpitaux (CRUD)                │               │
│   │  ○ Gérer les services (CRUD)                │               │
│   │  ○ Gérer les comptes utilisateurs           │               │
│   └─────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Diagramme de Séquence — Visiteur : géolocalisation + hôpitaux proches

```
Visiteur        Browser/JS         Django             API Opendatasoft
   │                │                  │                      │
   │  Ouvre le site │                  │                      │
   │───────────────>│  GET /           │                      │
   │                │─────────────────>│                      │
   │                │  home.html+carte │                      │
   │                │<─────────────────│                      │
   │                │                  │                      │
   │  [Auto]        │                  │                      │
   │  Geolocation   │                  │                      │
   │  API demande   │                  │                      │
   │  permission    │                  │                      │
   │<───────────────│                  │                      │
   │  Autorise      │                  │                      │
   │───────────────>│                  │                      │
   │                │  Position GPS    │                      │
   │                │  (lat, lon)      │                      │
   │                │                  │                      │
   │                │  GET /api/nearest│                      │
   │                │  ?lat=48&lon=2   │                      │
   │                │─────────────────>│                      │
   │                │                  │  GET records         │
   │                │                  │  ?where=num_dept=75  │
   │                │                  │─────────────────────>│
   │                │                  │  100 établissements  │
   │                │                  │<─────────────────────│
   │                │                  │                      │
   │                │                  │  Haversine(user,     │
   │                │                  │  chaque hôpital)     │
   │                │                  │  Tri par distance    │
   │                │                  │                      │
   │                │  JSON 50 hôpitaux│                      │
   │                │  triés par dist. │                      │
   │                │<─────────────────│                      │
   │                │                  │                      │
   │  Marqueur bleu │                  │                      │
   │  (position)    │                  │                      │
   │  Marqueurs     │                  │                      │
   │  violets       │                  │                      │
   │  (hôpitaux)    │                  │                      │
   │  Cards dans    │                  │                      │
   │  scroll area   │                  │                      │
   │<───────────────│                  │                      │
   │                │                  │                      │
   │  Filtre par    │                  │                      │
   │  catégorie     │                  │                      │
   │───────────────>│  [côté front]    │                      │
   │                │  filtre cards    │                      │
   │                │  + marqueurs     │                      │
   │  Vue filtrée   │                  │                      │
   │<───────────────│                  │                      │
```

---

## 5. Diagramme de Séquence — Staff met à jour les données

```
Staff Hôpital     Browser           Django View         Database
   │                 │                   │                  │
   │  Se connecter   │                   │                  │
   │────────────────>│  POST /login/     │                  │
   │                 │──────────────────>│                  │
   │                 │                   │  CHECK user/pass │
   │                 │                   │─────────────────>│
   │                 │                   │  OK              │
   │                 │                   │<─────────────────│
   │                 │  redirect /dash/  │                  │
   │                 │<──────────────────│                  │
   │                 │                   │                  │
   │  Voir dashboard │                   │                  │
   │────────────────>│  GET /dashboard/  │                  │
   │                 │──────────────────>│                  │
   │                 │                   │  SELECT services │
   │                 │                   │  WHERE hop=user  │
   │                 │                   │─────────────────>│
   │                 │                   │  mes services    │
   │                 │                   │<─────────────────│
   │                 │  dashboard.html   │                  │
   │                 │<──────────────────│                  │
   │                 │                   │                  │
   │  MAJ queue=15   │                   │                  │
   │────────────────>│  POST /dashboard/ │                  │
   │                 │──────────────────>│                  │
   │                 │                   │  UPDATE service  │
   │                 │                   │  SET queue=15    │
   │                 │                   │─────────────────>│
   │                 │                   │  OK              │
   │                 │                   │<─────────────────│
   │                 │  dashboard+succès │                  │
   │                 │<──────────────────│                  │
   │  Confirmé !     │                   │                  │
   │<────────────────│                   │                  │
```
