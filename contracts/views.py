from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .services import (
    OrganizationService, ClauseService, ContractService,
    TypeContractService, AreaService, PostService
)
from .models import Organization
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Clause, Organization, Area, TypeContract, Post, Contract
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


class ClauseView:
    @login_required
    @staticmethod
    def clauses_list(request):
        clauses = Clause.objects.all()
        Organizations = Organization.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'clauses/clause_list.html', {'clauses': clauses, 'organizations': Organizations, 'is_superadmin': is_superadmin})

    @login_required
    @staticmethod
    def create_clause(request):
        if request.method == 'POST':
            organization_id = request.POST.get('organization_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            print(organization_id, title, description)

            if not organization_id or not title or not description:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})

            try:
                organization = Organization.objects.get(id=organization_id)
            except Organization.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
            success, message = ClauseService.create_clause(
                organization, title, description)
            clauses = Clause.objects.select_related('organization').all()

            clauses_data = [
                {
                    'id': clause.id,
                    'organization': clause.organization.name,
                    'title': clause.title,
                    'description': clause.description,
                    'organization_id': clause.organization.id,
                    'created_at': clause.created_at,
                    'delete_url': reverse('delete_clause', args=[clause.id]),
                    'update_url': reverse('update_clause', args=[clause.id]),
                }
                for clause in clauses
            ]

            return JsonResponse({
                'success': success,
                'message': message,
                'clauses': clauses_data
            })

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @login_required
    @staticmethod
    def update_clause(request, clause_id):
        if request.method == 'POST':
            clause = Clause.objects.filter(id=clause_id).first()

            if not clause:
                return JsonResponse({'success': False, 'message': 'Cláusula no encontrada'}, status=404)

            title = request.POST.get('title')
            description = request.POST.get('description')
            organization_id = request.POST.get('organization_id')

            if not title or not description or not organization_id:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'}, status=400)

            success, message = ClauseService.update_clause(
                clause_id, title, description)

            if success:
                clauses = Clause.objects.select_related('organization').all()

                clauses_data = [
                    {
                        'id': clause.id,
                        'organization': clause.organization.name,
                        'title': clause.title,
                        'description': clause.description,
                        'organization_id': clause.organization.id,
                        'created_at': clause.created_at,
                        'delete_url': reverse('delete_clause', args=[clause.id]),
                        'update_url': reverse('update_clause', args=[clause.id]),
                    }
                    for clause in clauses
                ]
                return JsonResponse({'success': True, 'message': 'Cláusula actualizada correctamente', 'clauses': clauses_data})
            else:
                return JsonResponse({'success': False, 'message': message}, status=500)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @staticmethod
    @login_required
    def delete_clause(request, clause_id):
        if request.method == 'POST':
            success = ClauseService.delete_clause(clause_id)
            if success:
                clauses = Clause.objects.select_related('organization').all()

                clauses_data = [
                    {
                        'id': clause.id,
                        'organization': clause.organization.name,
                        'title': clause.title,
                        'description': clause.description,
                        'organization_id': clause.organization.id,
                        'created_at': clause.created_at,
                        'delete_url': reverse('delete_clause', args=[clause.id]),
                        'update_url': reverse('update_clause', args=[clause.id]),
                    }
                    for clause in clauses
                ]
                return JsonResponse({'success': True, 'message': 'Cláusula eliminada correctamente', 'clauses': clauses_data})
            else:
                return JsonResponse({'success': False, 'message': 'No se pudo eliminar la cláusula'}, status=400)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


class AreaView:
    @login_required
    @staticmethod
    def areas_list(request):
        areas = Area.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'areas/areas_list.html', {'areas': areas, 'is_superadmin': is_superadmin})

    @login_required
    @staticmethod
    def create_area(request):
        if request.method == 'POST':
            name_area = request.POST.get('name_area')
            if not name_area:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})

            success, message = AreaService.create_area(name_area)
            areas = Area.objects.all()

            areas_data = [
                {
                    'id': area.id,
                    'name_area': area.name_area,
                    'created_at': area.created_at,
                    'delete_url': reverse('delete_area', args=[area.id]),
                    'update_url': reverse('update_area', args=[area.id]),
                }
                for area in areas
            ]

            return JsonResponse({
                'success': success,
                'message': message,
                'areas': areas_data
            })

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @login_required
    @staticmethod
    def update_area(request, area_id):
        if request.method == 'POST':
            area = Area.objects.filter(id=area_id).first()

            if not area:
                return JsonResponse({'success': False, 'message': 'Área no encontrada'}, status=404)

            name_area = request.POST.get('name_area')

            if not name_area:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'}, status=400)

            success, message = AreaService.update_area(
                area_id, name_area)

            if success:
                areas = Area.objects.all()

                areas_data = [
                    {
                        'id': area.id,
                        'name_area': area.name_area,
                        'created_at': area.created_at,
                        'delete_url': reverse('delete_area', args=[area.id]),
                        'update_url': reverse('update_area', args=[area.id]),
                    }
                    for area in areas
                ]
                return JsonResponse({'success': True, 'message': 'Área actualizada correctamente', 'areas': areas_data})
            else:
                return JsonResponse({'success': False, 'message': message}, status=500)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @staticmethod
    @login_required
    def delete_area(request, area_id):
        if request.method == 'POST':
            success = AreaService.delete_area(area_id)
            if success:
                areas = Area.objects.all()

                areas_data = [
                    {
                        'id': area.id,
                        'name_area': area.name_area,
                        'created_at': area.created_at,
                        'delete_url': reverse('delete_area', args=[area.id]),
                        'update_url': reverse('update_area', args=[area.id]),
                    }
                    for area in areas
                ]
                return JsonResponse({'success': True, 'message': 'Área eliminada correctamente', 'areas': areas_data})
            else:
                return JsonResponse({'success': False, 'message': 'No se pudo eliminar el área'}, status=400)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


class TypeContractView:
    @login_required
    @staticmethod
    def typeC_list(request):
        typeContracts = TypeContract.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'type_contracts/typeContracts_list.html', {'typeContracts': typeContracts, 'is_superadmin': is_superadmin})

    @login_required
    @staticmethod
    def create_typeC(request):
        if request.method == 'POST':
            type_contract = request.POST.get('type_contract')
            if not type_contract:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})

            success, message = TypeContractService.create_type_contract(
                type_contract)
            tpye_contracts = TypeContract.objects.all()

            tpye_contracts_data = [
                {
                    'id': typeC.id,
                    'type_contract': typeC.type_contract,
                    'created_at': typeC.created_at,
                    'delete_url': reverse('delete_type_contract', args=[typeC.id]),
                    'update_url': reverse('update_type_contract', args=[typeC.id]),
                }
                for typeC in tpye_contracts
            ]

            return JsonResponse({
                'success': success,
                'message': message,
                'typeContracts': tpye_contracts_data
            })

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @login_required
    @staticmethod
    def update_typeC(request, typecon_id):
        if request.method == 'POST':
            typeC = TypeContract.objects.filter(id=typecon_id).first()

            if not typeC:
                return JsonResponse({'success': False, 'message': 'Tipo de Contrato no encontrado'}, status=404)

            type_contract = request.POST.get('type_contract')

            if not type_contract:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'}, status=400)

            success, message = TypeContractService.update_type_contract(
                typecon_id, type_contract)

            if success:
                type_contracts = TypeContract.objects.all()

                type_contracts_data = [
                    {
                        'id': typeC.id,
                        'type_contract': typeC.type_contract,
                        'created_at': typeC.created_at,
                        'delete_url': reverse('delete_type_contract', args=[typeC.id]),
                        'update_url': reverse('update_type_contract', args=[typeC.id]),
                    }
                    for typeC in type_contracts
                ]
                return JsonResponse({'success': True, 'message': 'Tipo de Contrato actualizado correctamente', 'typeContracts': type_contracts_data})
            else:
                return JsonResponse({'success': False, 'message': message}, status=500)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @staticmethod
    @login_required
    def delete_typeC(request, typecon_id):
        if request.method == 'POST':
            success = TypeContractService.delete_type_contract(typecon_id)
            if success:
                type_contracts = TypeContract.objects.all()

                type_contracts_data = [
                    {
                        'id': typeC.id,
                        'type_contract': typeC.type_contract,
                        'created_at': typeC.created_at,
                        'delete_url': reverse('delete_type_contract', args=[typeC.id]),
                        'update_url': reverse('update_type_contract', args=[typeC.id]),
                    }
                    for typeC in type_contracts
                ]
                return JsonResponse({'success': True, 'message': 'Tipo de Contrato eliminado correctamente', 'typeContracts': type_contracts_data})
            else:
                return JsonResponse({'success': False, 'message': 'No se pudo eliminar el Tipo de Contrato'}, status=400)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


class PostView:
    @login_required
    @staticmethod
    def posts_list(request):
        posts = Post.objects.all()
        areas = Area.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'posts/posts_list.html', {'posts': posts, 'areas': areas, 'is_superadmin': is_superadmin})

    @login_required
    @staticmethod
    def create_post(request):
        if request.method == 'POST':
            area_id = request.POST.get('area_id')
            name_posts = request.POST.get('name_posts')

            if not area_id or not name_posts:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})

            try:
                area = Area.objects.get(id=area_id)
            except Area.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Área no encontrada'})
            success, message = PostService.create_post(
                area, name_posts)
            posts = Post.objects.select_related('area').all()

            posts_data = [
                {
                    'id': post.id,
                    'area': post.area.name_area,
                    'name_posts': post.name_posts,
                    'area_id': post.area.id,
                    'created_at': post.created_at,
                    'delete_url': reverse('delete_post', args=[post.id]),
                    'update_url': reverse('update_post', args=[post.id]),
                }
                for post in posts
            ]

            return JsonResponse({
                'success': success,
                'message': message,
                'posts': posts_data
            })

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @login_required
    @staticmethod
    def update_post(request, post_id):
        if request.method == 'POST':
            post = Post.objects.filter(id=post_id).first()

            if not post:
                return JsonResponse({'success': False, 'message': 'Cargo no encontrado'}, status=404)

            name_posts = request.POST.get('name_posts')
            area_id = request.POST.get('area_id')

            if not name_posts or not area_id:
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'}, status=400)

            success, message = PostService.update_post(
                post_id, name_posts)

            if success:
                posts = Post.objects.select_related('area').all()

                posts_data = [
                    {
                        'id': post.id,
                        'area': post.area.name_area,
                        'name_posts': post.name_posts,
                        'area_id': post.area.id,
                        'created_at': post.created_at,
                        'delete_url': reverse('delete_post', args=[post.id]),
                        'update_url': reverse('update_post', args=[post.id]),
                    }
                    for post in posts
                ]
                return JsonResponse({'success': True, 'message': 'Cargo actualizado correctamente', 'posts': posts_data})
            else:
                return JsonResponse({'success': False, 'message': message}, status=500)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @staticmethod
    @login_required
    def delete_post(request, post_id):
        if request.method == 'POST':
            success = PostService.delete_post(post_id)
            if success:
                posts = Post.objects.select_related('area').all()

                posts_data = [
                    {
                        'id': post.id,
                        'area': post.area.name_area,
                        'name_posts': post.name_posts,
                        'area_id': post.area.id,
                        'created_at': post.created_at,
                        'delete_url': reverse('delete_post', args=[post.id]),
                        'update_url': reverse('update_post', args=[post.id]),
                    }
                    for post in posts
                ]
                return JsonResponse({'success': True, 'message': 'Cargo eliminado correctamente', 'posts': posts_data})
            else:
                return JsonResponse({'success': False, 'message': 'No se pudo eliminar el Cargo'}, status=400)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    
class ContractView:
    @login_required
    @staticmethod
    def contracts_list(request):
        contracts = Contract.objects.all()
        users = User.objects.exclude(id=request.user.id)
        organization = Organization.objects.all()
        typeContract = TypeContract.objects.all()
        post = Post.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'contracts/contracts_list.html', {
            'contracts': contracts, 
            'users': users, 
            'is_superadmin': is_superadmin, 
            'organization':organization,
            'typeContract':typeContract,
            'post':post,
            })
    
    @login_required
    @staticmethod
    def contracts_create(request):
        contracts = Contract.objects.all()
        users = User.objects.exclude(id=request.user.id)
        organizations = Organization.objects.all()
        typeContracts = TypeContract.objects.all()
        clauses = Clause.objects.all()
        posts = Post.objects.all()
        is_superadmin = request.user.groups.filter(
            name='superAdministrators').exists()
        return render(request, 'contracts/contracts_create.html', {
            'contracts': contracts, 
            'users': users, 
            'is_superadmin': is_superadmin, 
            'organizations':organizations,
            'typeContracts':typeContracts,
            'posts':posts,
            'clauses':clauses,
            })