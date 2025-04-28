from django.contrib.auth.models import User
from .repositories import (
    OrganizationRepository, ClauseRepository,
    ContractRepository, TypeContractRepository, AreaRepository, PostRepository
)
from .models import ContractClause, Organization, Notification
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .observers import ContractCreatedEvent
from django.contrib.auth.models import Group

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
        return ClauseRepository.create_clause(organization, title, description)

    @staticmethod
    def update_clause(clause_id, title, description):
        return ClauseRepository.edit_clause(clause_id, title, description)

    @staticmethod
    def delete_clause(clause_id):
        return ClauseRepository.delete_clause(clause_id)


class ContractService:
    @staticmethod
    @transaction.atomic
    def create_contract_with_clauses(contract_data, clauses_data):
        contract = ContractRepository.create_contract(contract_data)
        ContractRepository.create_clauses(contract, clauses_data)
        
        ContractCreatedEvent.notify(contract)
        gerente_group = Group.objects.get(name='GERENTE')

        gerentes = gerente_group.user_set.all()

        for gerente in gerentes:
            NotificationService.create_notification(
                user=gerente,
                message="Tienes un contrato pendiente por revisar.",
                contract=contract
            )
        return contract
    @staticmethod
    def approve_contract(contract_id):
        return ContractRepository.approve_contract(contract_id)
    
    @staticmethod
    def get_contract_with_clauses(contract_id):
        return ContractRepository.get_contract_with_clauses(contract_id)

class NotificationService:
    @staticmethod
    def create_notification(user, message, contract):
        notification = Notification(
            user=user,
            message=message,
            is_read=False
        )
        notification.save()


class TypeContractService:
    @staticmethod
    def create_type_contract(type_contract):
        return TypeContractRepository.create_type_contract(type_contract)

    @staticmethod
    def update_type_contract(typecon_id, type_contract):
        return TypeContractRepository.update_type_contract(typecon_id, type_contract)

    @staticmethod
    def delete_type_contract(typecon_id):
        return TypeContractRepository.delete_type_contract(typecon_id)


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
    def create_post(area, name_posts):
        return PostRepository.create_post(area, name_posts)

    @staticmethod
    def update_post(post_id, name_posts):
        return PostRepository.edit_post(post_id, name_posts)

    @staticmethod
    def delete_post(post_id):
        return PostRepository.delete_post(post_id)
