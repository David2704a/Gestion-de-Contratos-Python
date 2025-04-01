from .repositories import (
    OrganizationRepository, ClauseRepository, UserRepository,
    ContractRepository, TypeContractRepository, AreaRepository, PostRepository
)
from .models import ContractClause, ExtendedUser


class OrganizationService:
    @staticmethod
    def create_organization(data):
        return OrganizationRepository.create_organization(data)

    @staticmethod
    def edit_organization(org_id, data):
        return OrganizationRepository.edit_organization(org_id, data)


class ClauseService:
    @staticmethod
    def create_clause(data):
        return ClauseRepository.create_clause(data)

    @staticmethod
    def edit_clause(clause_id, data):
        return ClauseRepository.edit_clause(clause_id, data)


class UserService:
    @staticmethod
    def create_user(data):
        user = UserRepository.create_user(data)
        ExtendedUser.objects.create(
            user=user,
            phone_number=data['phone_number'],
            identification_number=data['identification_number'],
            birth_date=data['birth_date'],
            address=data['address'],
            type_identification_id=data['type_identification'],
            organization_id=data['organization']
        )
        return user

    @staticmethod
    def edit_user(user_id, data):
        return UserRepository.edit_user(user_id, data)


class ContractService:
    @staticmethod
    def create_contract(data):
        contract = ContractRepository.create_contract(data)
        # Agregar cláusulas elegidas al contrato
        for clause_id in data['clauses']:
            ContractClause.objects.create(
                contract=contract, clause_id=clause_id)
        return contract

    @staticmethod
    def approve_contract(contract_id):
        return ContractRepository.approve_contract(contract_id)


class TypeContractService:
    @staticmethod
    def create_type_contract(data):
        return TypeContractRepository.create_type_contract(data)


class AreaService:
    @staticmethod
    def create_area(data):
        return AreaRepository.create_area(data)


class PostService:
    @staticmethod
    def create_post(data):
        return PostRepository.create_post(data)
