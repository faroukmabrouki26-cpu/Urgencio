import json

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ServiceUpdateForm
from .models import Hospital, Service


def home(request):
    hospitals = Hospital.objects.prefetch_related('services').all()
    hospitals_json = json.dumps([
        {
            'id': h.id,
            'name': h.name,
            'city': h.city,
            'lat': h.latitude,
            'lng': h.longitude,
            'available': h.is_any_service_available(),
        }
        for h in hospitals
    ])
    return render(request, 'hospitals/home.html', {
        'hospitals': hospitals,
        'hospitals_json': hospitals_json,
    })


def hospital_list(request):
    hospitals = Hospital.objects.prefetch_related('services').all()
    city = request.GET.get('city', '').strip()
    search = request.GET.get('q', '').strip()
    if city:
        hospitals = hospitals.filter(city__icontains=city)
    if search:
        hospitals = hospitals.filter(name__icontains=search)
    cities = Hospital.objects.values_list('city', flat=True).distinct().order_by('city')
    return render(request, 'hospitals/hospital_list.html', {
        'hospitals': hospitals,
        'cities': cities,
        'current_city': city,
        'search_query': search,
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
