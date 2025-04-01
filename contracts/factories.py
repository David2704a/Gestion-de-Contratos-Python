from .models import Contract

class ContractFactory:
    @staticmethod
    def create_contract(user, organization, type_contract, salary, post):
        return Contract.objects.create(
            user=user,
            organization=organization,
            type_contract=type_contract,
            salary=salary,
            post=post,
            status='PENDIENTE'
        )
