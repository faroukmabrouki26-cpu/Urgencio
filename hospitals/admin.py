from django.contrib import admin
from .models import Hospital, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'arrondissement', 'phone', 'is_any_service_available')
    list_filter = ('arrondissement',)
    search_fields = ('name', 'address')
    inlines = [ServiceInline]

    def is_any_service_available(self, obj):
        return obj.is_any_service_available()
    is_any_service_available.boolean = True
    is_any_service_available.short_description = 'Disponible'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'is_available', 'queue_count', 'estimated_wait_time', 'last_updated')
    list_filter = ('name', 'is_available', 'hospital')
    search_fields = ('hospital__name',)
