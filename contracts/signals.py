from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contract

@receiver(post_save, sender=Contract)
def notify_user_contract_status(sender, instance, **kwargs):
    print(f"El contrato {instance.id} cambió a {instance.status}")
