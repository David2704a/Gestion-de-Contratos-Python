from django.db import models
from django.contrib.auth.models import User
from contracts.models import Organization
from django.utils import timezone

# Tipo de Identificación
class TypeIdentification(models.Model):
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description

# Usuario extendido


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    identification_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    address = models.TextField()
    type_identification = models.ForeignKey(
        TypeIdentification, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username