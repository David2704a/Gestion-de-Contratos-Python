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
    def create_clause(data):
        return ClauseRepository.create_clause(data)

    @staticmethod
    def edit_clause(clause_id, data):
        return ClauseRepository.edit_clause(clause_id, data)


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
