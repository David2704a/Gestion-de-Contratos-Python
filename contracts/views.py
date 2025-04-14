from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .services import (
    OrganizationService, ClauseService, ContractService,
    TypeContractService, AreaService, PostService
)
from .models import Organization
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Clause, Organization
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


class ClauseView:
    @login_required
    @staticmethod
    def clauses_list(request):
        clauses = Clause.objects.all()
        Organizations = Organization.objects.all()
        return render(request, 'clauses/clause_list.html', {'clauses': clauses, 'organizations': Organizations})

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
            clauses = Clause.objects.all()
            clauses_data = [
                {
                    'id': clause.id,
                    'organization': clause.organization.name,
                    'title': clause.title,
                    'description': clause.description,
                    'created_at': clause.created_at
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
                return JsonResponse({'success': True, 'message': 'Cláusula actualizada correctamente'})
            else:
                return JsonResponse({'success': False, 'message': message}, status=500)

        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    @staticmethod
    @login_required
    def delete_clause(request, clause_id):
        if request.method == 'POST':
            success = ClauseService.delete_clause(clause_id)
            if success:
                clauses = Clause.objects.all()
                clauses_data = [
                    {
                        'id': clause.id,
                        'organization': clause.organization.name,
                        'title': clause.title,
                        'description': clause.description,
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
