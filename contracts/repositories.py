from .models import Organization, Clause, Contract, TypeContract, Post, Area
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
    def create_clause(organization, title, description):
        try:
            # Creamos una nueva cláusula y la guardamos
            clause = Clause.objects.create(
                organization=organization,
                title=title,
                description=description
            )
            return True, "Cláusula creada exitosamente."
        except Exception as e:
            return False, f"Error al crear la cláusula: {str(e)}"

    @staticmethod
    def edit_clause(clause_id, title, description):
        try:
            clause = Clause.objects.get(id=clause_id)
            clause.title = title
            clause.description = description
            clause.save()
            return True, "Cláusula actualizada exitosamente."
        except Clause.DoesNotExist:
            return False, "La cláusula no existe."
        except Exception as e:
            return False, f"Error al actualizar la cláusula: {str(e)}"

    @staticmethod
    def delete_clause(clause_id):
        try:
            # Encontramos y eliminamos la cláusula
            clause = Clause.objects.get(id=clause_id)
            clause.delete()
            return True
        except Clause.DoesNotExist:
            return False
        except Exception as e:
            return False


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
    def create_type_contract(type_contract):
        try:
            type_con = TypeContract.objects.create(
                type_contract=type_contract,
            )
            return True, "Tipo de Contrato creado exitosamente."
        except Exception as e:
            return False, f"Error al crear el Tipo de Contrato: {str(e)}"

    @staticmethod
    def update_type_contract(typecon_id, type_contract,):
        try:
            typeC = TypeContract.objects.get(id=typecon_id)
            typeC.type_contract = type_contract
            typeC.save()
            return True, "Tipo de Contrato actualizado exitosamente."
        except Area.DoesNotExist:
            return False, "El Tipo de Contrato no existe."
        except Exception as e:
            return False, f"Error al actualizar el Tipo de Contrato: {str(e)}"

    @staticmethod
    def delete_type_contract(typecon_id):
        try:
            typeC = TypeContract.objects.get(id=typecon_id)
            typeC.delete()
            return True
        except TypeContract.DoesNotExist:
            return False
        except Exception as e:
            return False


class AreaRepository:
    @staticmethod
    def create_area(name_area):
        try:
            area = Area.objects.create(
                name_area=name_area,
            )
            return True, "Área creada exitosamente."
        except Exception as e:
            return False, f"Error al crear el área: {str(e)}"

    @staticmethod
    def edit_area(area_id, name_area,):
        try:
            area = Area.objects.get(id=area_id)
            area.name_area = name_area
            area.save()
            return True, "Área actualizada exitosamente."
        except Area.DoesNotExist:
            return False, "El área no existe."
        except Exception as e:
            return False, f"Error al actualizar el área: {str(e)}"

    @staticmethod
    def delete_area(area_id):
        try:
            area = Area.objects.get(id=area_id)
            area.delete()
            return True
        except Area.DoesNotExist:
            return False
        except Exception as e:
            return False


class PostRepository:
    @staticmethod
    def create_post(area, name_posts):
        try:
            post = Post.objects.create(
                area=area,
                name_posts=name_posts,
            )
            return True, "Cargo creada exitosamente."
        except Exception as e:
            return False, f"Error al crear el Cargo: {str(e)}"

    @staticmethod
    def edit_post(post_id, name_posts):
        try:
            post = Post.objects.get(id=post_id)
            post.name_posts = name_posts
            post.save()
            return True, "Cargo actualizado exitosamente."
        except Post.DoesNotExist:
            return False, "El cargo no existe."
        except Exception as e:
            return False, f"Error al actualizar el Cargo: {str(e)}"

    @staticmethod
    def delete_post(post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return True
        except Post.DoesNotExist:
            return False
        except Exception as e:
            return False
