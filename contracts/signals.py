from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Contract
from django.apps import apps


# @receiver(post_save, sender=Contract)
# def notify_user_contract_status(sender, instance, **kwargs):
#     print(f"El contrato {instance.id} cambió a {instance.status}")


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    print(f"Ejecutando señal en 1: {sender.name}")

    if sender.name == "contracts":
        group_names = ["Administrators", "Accountants",
                       "Collaborators", "Human Resources", "Lawyers"]

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Grupo '{group_name}' creado correctamente.")

                if group_name == "Administradores":
                    permissions = Permission.objects.all()
                    group.permissions.set(permissions)
                    print(f"Permisos asignados a '{group_name}'.")

        print("Grupos creados exitosamente.")


@receiver(post_migrate)
def create_test_organizations(sender, **kwargs):
    print(f"Ejecutando señal en 2: {sender.name}")

    if sender.name == "contracts":
        Organization = apps.get_model('contracts', 'Organization')

        organizations = [
            {
                "name": "Empresa ABC S.A.",
                "address": "Calle 123 #45-67, Bogotá",
                "nit": "900123456-7",
                "contact_info": "Juan Pérez",
                "email": "contacto@empresaabc.com"
            },
            {
                "name": "Tecnologías XYZ Ltda.",
                "address": "Avenida Principal 890, Medellín",
                "nit": "800987654-3",
                "contact_info": "María Gómez",
                "email": "info@tecnologiasxyz.com"
            },
            {
                "name": "Servicios Generales QWERTY",
                "address": "Carrera 56 #12-34, Cali",
                "nit": "890654321-1",
                "contact_info": "Carlos Rodríguez",
                "email": "servicios@qwerty.com"
            }
        ]

        for org in organizations:
            obj, created = Organization.objects.get_or_create(
                nit=org["nit"],
                defaults={
                    "name": org["name"],
                    "address": org["address"],
                    "contact_info": org["contact_info"],
                    "email": org["email"]
                }
            )
            if created:
                print(
                    f"Organización '{org['name']}' creada con NIT: {org['nit']}")

        print("Organizaciones de prueba creadas exitosamente.")
