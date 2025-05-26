from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from .services import NotificationService
from datetime import date


class Observer:
    def update(self, contract):
        raise NotImplementedError(
            "Debe implementar el método update() en la clase observadora")


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


class ContractEndingSoonEvent:
    observers = []

    @classmethod
    def subscribe(cls, observer):
        cls.observers.append(observer)

    @classmethod
    def notify(cls, contract):
        for observer in cls.observers:
            observer.update(contract)


class LegalNotificationObserver(Observer):
    def update(self, contract):
        print('entrooooo')
        today = date.today()
        if contract.end_date:
            days_remaining = (contract.end_date - today).days
        else:
            days_remaining = None

        if days_remaining is not None and days_remaining <= 35:
            try:
                juridico_group = Group.objects.get(name="Lawyers")
                juridicos = juridico_group.user_set.all()

                for juridico in juridicos:
                    # Notificación in-app
                    NotificationService.create_notification(
                        user=juridico,
                        message=f"El contrato de {contract.user.get_full_name()} está por finalizar en {days_remaining} días.",
                    )

                    # Email
                    send_mail(
                        subject="Contrato por finalizar",
                        message=f"Hola {juridico.first_name},\n\nEl contrato de {contract.user.get_full_name()} finaliza el {contract.end_date}.\nFaltan {days_remaining} días.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[juridico.email],
                        fail_silently=False,
                    )
            except Group.DoesNotExist:
                print("No existe el grupo Jurídico")
