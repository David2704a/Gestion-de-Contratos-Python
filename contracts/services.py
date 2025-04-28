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
    def __init__(self, contract_repository, notification_service):
        self.repository = contract_repository
        self.notification_service = notification_service
        
    def create_contract(self, contract_data, clauses_data):
        """
        Crea un nuevo contrato con sus cláusulas y notifica a los gerentes
        Args:
            contract_data: Diccionario con datos del contrato
            clauses_data: Lista de diccionarios con cláusulas
        Returns:
            Contrato creado
        """
        self._validate_contract_data(contract_data)
        self._validate_clauses(clauses_data)
        
        with transaction.atomic():
            contract = self.repository.create(contract_data)
            self.repository.add_clauses(contract, clauses_data)
            self._notify_managers(contract)
            
        return contract
    
    def _notify_managers(self, contract):
        """Notifica a todos los gerentes sobre el nuevo contrato"""
        managers_group = Group.objects.get(name='GERENTE')
        message = f"Nuevo contrato creado ({contract.get_type_display()}) requiere revisión"
        
        for manager in managers_group.user_set.all():
            self.notification_service.create(
                user=manager,
                message=message,
                contract=contract
            )
    
    def approve_contract(self, contract_id):
        contract = self.repository.update(
            contract_id, 
            approval='APROBADO'
        )
        self._notify_approval(contract)
        return contract
    
    def _validate_contract_data(self, data):
        required_fields = ['user', 'organization', 'type_contract', 'post']
        if not all(data.get(field) for field in required_fields):
            raise ValueError("Todos los campos obligatorios deben estar completos")
    
    def _validate_clauses(self, clauses):
        if not clauses:
            raise ValueError("Debe agregar al menos una cláusula")
    
    def _notify_managers(self, contract):
        managers = Group.objects.get(name='GERENTE').user_set.all()
        for manager in managers:
            NotificationService.create(
                user=manager,
                message="Tienes un contrato pendiente por revisar",
                contract=contract
            )
            
    def get_contract_with_clauses(contract_id):
        return ContractRepository.get_contract_with_clauses(contract_id)
    
    def get_contract_details(self, contract_id):
        contract = self.repository.get_by_id(contract_id)
        clauses = ContractClause.objects.filter(contract=contract)
        return contract, clauses

class NotificationService:
    def __init__(self, notification_model):
        self.model = notification_model
    
    def create(self, user, message, contract=None, is_read=False):

        notification = self.model(
            user=user,
            message=message,
            contract=contract,
            is_read=is_read
        )
        notification.save()
        return notification
    
    def mark_as_read(self, notification_id):
        """Marca una notificación como leída"""
        notification = self.model.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return notification


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
