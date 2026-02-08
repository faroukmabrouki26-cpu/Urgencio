import json
import logging
from urllib.parse import urlencode
from urllib.request import urlopen

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ServiceUpdateForm
from .models import Hospital, Service
from .utils import haversine

logger = logging.getLogger(__name__)

OPENDATASOFT_API_URL = (
    "https://data.iledefrance.fr/api/explore/v2.1/catalog/datasets/"
    "les_etablissements_hospitaliers_franciliens/records"
)


def home(request):
    return render(request, 'hospitals/home.html')


def hospital_list(request):
    hospitals = Hospital.objects.prefetch_related('services').all()
    arrondissement = request.GET.get('arrondissement', '').strip()
    type_urgence = request.GET.get('type', '').strip()
    search = request.GET.get('q', '').strip()

    if arrondissement:
        hospitals = hospitals.filter(arrondissement=arrondissement)
    if type_urgence:
        hospitals = hospitals.filter(services__name=type_urgence).distinct()
    if search:
        hospitals = hospitals.filter(name__icontains=search)

    arrondissements = Hospital.objects.values_list('arrondissement', flat=True).distinct().order_by('arrondissement')
    hospitals = hospitals[:30]

    return render(request, 'hospitals/hospital_list.html', {
        'hospitals': hospitals,
        'arrondissements': arrondissements,
        'current_arrondissement': arrondissement,
        'current_type': type_urgence,
        'search_query': search,
        'type_choices': Service.TYPE_CHOICES,
    })


def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital.objects.prefetch_related('services'), pk=pk)
    return render(request, 'hospitals/hospital_detail.html', {
        'hospital': hospital,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'hospitals/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    try:
        hospital = request.user.hospital
    except Hospital.DoesNotExist:
        messages.error(request, "Aucun hôpital n'est associé à votre compte.")
        return redirect('home')

    ServiceFormSet = modelformset_factory(
        Service, form=ServiceUpdateForm, extra=0
    )

    services = hospital.services.all()

    if request.method == 'POST':
        formset = ServiceFormSet(request.POST, queryset=services)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Données mises à jour avec succès !')
            return redirect('dashboard')
    else:
        formset = ServiceFormSet(queryset=services)

    return render(request, 'hospitals/dashboard.html', {
        'hospital': hospital,
        'formset': formset,
    })


def nearest_hospitals(request):
    """Endpoint JSON : renvoie les hôpitaux IDF les plus proches via l'API Opendatasoft."""
    try:
        lat = float(request.GET.get('lat', ''))
        lon = float(request.GET.get('lon', ''))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Paramètres lat et lon requis.'}, status=400)

    limit = min(int(request.GET.get('limit', 10)), 50)

    # Requête vers l'API Opendatasoft — filtrer sur Paris (dept 75)
    params = urlencode({
        'limit': 100,
        'where': 'num_dept=75',
        'select': 'raison_sociale,adresse_complete,cp_ville,num_tel,categorie_de_l_etablissement,lat,lng',
    })
    url = f"{OPENDATASOFT_API_URL}?{params}"

    try:
        with urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        logger.error("Erreur API Opendatasoft: %s", e)
        return JsonResponse({'error': "Impossible de contacter l'API externe."}, status=502)

    results = []
    for record in data.get('results', []):
        r_lat = record.get('lat')
        r_lng = record.get('lng')
        if r_lat is None or r_lng is None:
            continue
        try:
            r_lat = float(r_lat)
            r_lng = float(r_lng)
        except (ValueError, TypeError):
            continue

        distance = haversine(lat, lon, r_lat, r_lng)
        results.append({
            'name': record.get('raison_sociale', ''),
            'address': record.get('adresse_complete', '') or '',
            'city': record.get('cp_ville', ''),
            'phone': record.get('num_tel', '') or '',
            'category': record.get('categorie_de_l_etablissement', ''),
            'lat': r_lat,
            'lng': r_lng,
            'distance_km': round(distance, 2),
        })

    results.sort(key=lambda x: x['distance_km'])
    return JsonResponse({'hospitals': results[:limit]})
