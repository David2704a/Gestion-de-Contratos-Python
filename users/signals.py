from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import TypeIdentification
from django.apps import apps
@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    print(f"Ejecutando señal en creacion user: {sender.name}")
    if sender.name == "users":
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@example.com", "admin123")
            print("Superusuario creado automáticamente")

@receiver(post_migrate)
def create_type_identifications(sender, **kwargs):
    print(f"Ejecutando señal en creacion abreviation: {sender.name}")

    if sender.name == "users":
        identifications = [
            {"abbreviation": "CC", "description": "Cédula de Ciudadanía"},
            {"abbreviation": "TI", "description": "Tarjeta de Identidad"},
            {"abbreviation": "CE", "description": "Cédula de Extranjería"},
            {"abbreviation": "NIT", "description": "Número de Identificación Tributaria"},
        ]

        for ident in identifications:
            obj, created = TypeIdentification.objects.get_or_create(
                abbreviation=ident["abbreviation"],
                defaults={"description": ident["description"]}
            )
            if created:
                print(
                    f"Tipo de identificación '{ident['abbreviation']}' creado.")

        print("Registros de Type_identification creados exitosamente.")