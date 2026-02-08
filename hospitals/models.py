from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital')

    def get_services(self):
        return self.services.all()

    def is_any_service_available(self):
        return self.services.filter(is_available=True).exists()

    def __str__(self):
        return self.name


class Service(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    queue_count = models.PositiveIntegerField(default=0)
    estimated_wait_time = models.PositiveIntegerField(default=0, help_text="Temps d'attente estimé en minutes")
    last_updated = models.DateTimeField(auto_now=True)

    def update_queue(self, count, wait_time):
        self.queue_count = count
        self.estimated_wait_time = wait_time
        self.save()

    def toggle_availability(self):
        self.is_available = not self.is_available
        self.save()

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"
