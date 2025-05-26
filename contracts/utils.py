def check_contracts_ending_soon():
    print("Verificando contratos por vencer...")  # prueba
    from .models import Contract
    from .observers import ContractEndingSoonEvent
    from datetime import date

    today = date.today()
    contracts = Contract.objects.filter(end_date__isnull=False)

    for contract in contracts:
        days_remaining = (contract.end_date - today).days
        if days_remaining <= 35:
            print(f"Contrato de {contract.user} termina en {days_remaining} días")  # prueba
            ContractEndingSoonEvent.notify(contract)
