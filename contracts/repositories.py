from .models import Organization, Clause, TypeIdentification, Contract, TypeContract, Post, Area
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class OrganizationRepository:
    @staticmethod
    def get_organizations():
        return Organization.objects.all()

    @staticmethod
    def get_organization(org_id):
        try:
            return Organization.objects.get(id=org_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_organization(data):
        return Organization.objects.create(**data)

    @staticmethod
    def edit_organization(org_id, data):
        organization = OrganizationRepository.get_organization(org_id)
        if organization:
            for key, value in data.items():
                setattr(organization, key, value)
            organization.save()
        return organization


class ClauseRepository:
    @staticmethod
    def get_clauses():
        return Clause.objects.all()

    @staticmethod
    def create_clause(data):
        return Clause.objects.create(**data)

    @staticmethod
    def edit_clause(clause_id, data):
        clause = Clause.objects.get(id=clause_id)
        for key, value in data.items():
            setattr(clause, key, value)
        clause.save()
        return clause


class UserRepository:
    @staticmethod
    def get_users():
        return User.objects.all()

    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_user(data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return user

    @staticmethod
    def edit_user(user_id, data):
        user = User.objects.get(id=user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user


class ContractRepository:
    @staticmethod
    def get_contracts():
        return Contract.objects.all()

    @staticmethod
    def get_contract(contract_id):
        return Contract.objects.get(id=contract_id)

    @staticmethod
    def create_contract(data):
        return Contract.objects.create(**data)

    @staticmethod
    def edit_contract(contract_id, data):
        contract = Contract.objects.get(id=contract_id)
        for key, value in data.items():
            setattr(contract, key, value)
        contract.save()
        return contract

    @staticmethod
    def approve_contract(contract_id):
        contract = Contract.objects.get(id=contract_id)
        contract.approval = 'APROBADO'
        contract.save()
        return contract

    @staticmethod
    def obtain_contracts_to_finalize():
        return Contract.objects.filter(status='POR FINALIZAR')

# Repositorios para otras entidades


class TypeContractRepository:
    @staticmethod
    def get_type_contract():
        return TypeContract.objects.all()

    @staticmethod
    def create_type_contract(data):
        return TypeContract.objects.create(**data)


class AreaRepository:
    @staticmethod
    def get_areas():
        return Area.objects.all()

    @staticmethod
    def create_area(data):
        return Area.objects.create(**data)


class PostRepository:
    @staticmethod
    def get_posts():
        return Post.objects.all()

    @staticmethod
    def create_post(data):
        return Post.objects.create(**data)
