from django.contrib.auth.models import User
from .repositories import (
    OrganizationRepository, ClauseRepository, UserRepository,
    ContractRepository, TypeContractRepository, AreaRepository, PostRepository
)
from .models import ContractClause, ExtendedUser, Organization, TypeIdentification
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404

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
        """ Crea un usuario en User y lo asocia con ExtendedUser """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        identification_number = data.get('identification_number')
        birth_date = data.get('birth_date')
        address = data.get('address')
        type_identification_id = data.get('type_identification_id')
        organization_id = data.get('organization_id')

        if User.objects.filter(username=username).exists():
            return False, "El nombre de usuario ya está en uso."
        if User.objects.filter(email=email).exists():
            return False, "El correo electrónico ya está registrado."
        if ExtendedUser.objects.filter(identification_number=identification_number).exists():
            return False, "El número de identificación ya está en uso."

        # Crear usuario en auth_user
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

        # Obtener las relaciones con otras tablas
        type_identification = TypeIdentification.objects.get(
            id=type_identification_id)
        organization = Organization.objects.get(id=organization_id)

        # Crear el usuario extendido
        ExtendedUser.objects.create(
            user=user,
            phone_number=phone_number,
            identification_number=identification_number,
            birth_date=birth_date,
            address=address,
            type_identification=type_identification,
            organization=organization
        )

        return True, "Usuario creado exitosamente."

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
