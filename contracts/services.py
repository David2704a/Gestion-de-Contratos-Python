from django.contrib.auth.models import User
from .repositories import (
    OrganizationRepository, ClauseRepository,
    ContractRepository, TypeContractRepository, AreaRepository, PostRepository
)
from .models import ContractClause, Organization
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
    def create_clause(organization, title, description):
        # Llamamos al repositorio para crear la cláusula
        return ClauseRepository.create_clause(organization, title, description)

    @staticmethod
    def update_clause(clause_id, title, description):
        # Llamamos al repositorio para editar la cláusula
        return ClauseRepository.edit_clause(clause_id, title, description)

    @staticmethod
    def delete_clause(clause_id):
        # Llamamos al repositorio para eliminar la cláusula
        return ClauseRepository.delete_clause(clause_id)



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
    def create_area(name_area):
        return AreaRepository.create_area(name_area)

    @staticmethod
    def update_area(area_id, name_area):
        return AreaRepository.edit_area(area_id, name_area)

    @staticmethod
    def delete_area(area_id):
        return AreaRepository.delete_area(area_id)

class PostService:
    @staticmethod
    def create_post(data):
        return PostRepository.create_post(data)
