from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

class Observer:
    def update(self, contract):
        raise NotImplementedError("Debe implementar el método update() en la clase observadora")

class ContractCreatedEvent:
    observers = []

    @classmethod
    def subscribe(cls, observer):
        cls.observers.append(observer)

    @classmethod
    def notify(cls, contract):
        for observer in cls.observers:
            observer.update(contract)

class EmailNotificationObserver(Observer):
    def update(self, contract):
        try:
            gerente_group = Group.objects.get(name="Gerente")
            gerentes = gerente_group.user_set.all()
            for gerente in gerentes:
                send_mail(
                    subject="Nuevo contrato pendiente de revisión",
                    message=f"Hola {gerente.first_name},\n\nSe ha creado un nuevo contrato para revisar.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[gerente.email],
                    fail_silently=False,
                )
        except Group.DoesNotExist:
            print("No existe el grupo GERENTE")
