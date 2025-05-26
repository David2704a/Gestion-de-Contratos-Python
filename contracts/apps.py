from django.apps import AppConfig

class ContractsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contracts'

    def ready(self):
        import contracts.signals
        from . import observers
        from .utils import check_contracts_ending_soon
        check_contracts_ending_soon()

        observers.ContractCreatedEvent.subscribe(observers.EmailNotificationObserver())
        observers.ContractEndingSoonEvent.subscribe(observers.LegalNotificationObserver())