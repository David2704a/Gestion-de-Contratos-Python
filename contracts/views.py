from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .services import (
    OrganizationService, ClauseService, ContractService,
    TypeContractService, AreaService, PostService
)
from .models import Organization
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Clause, Organization
from django.http import HttpResponse
from .forms import ClauseForm
from django.template.loader import render_to_string

class ClauseView:
    @login_required
    @staticmethod
    def clauses_list(request):
        clauses = Clause.objects.all()
        return render(request, 'clauses/clause_list.html', {'clauses': clauses})

    @login_required
    @staticmethod
    # def create_clause(request):
    #     if request.method == 'POST':
    #         organization_id = request.POST.get('organization_id')
    #         title = request.POST.get('title')
    #         description = request.POST.get('description')
    #         print(organization_id, title, description, 'alo1')

    #         # Validamos si los datos necesarios están presentes
    #         if not organization_id or not title or not description:
    #             return render(request, 'clauses/clause_create.html', {'error': 'Todos los campos son obligatorios'})

    #         organization = Organization.objects.get(id=organization_id)

    #         # Usamos ClauseService para crear la cláusula
            
    #         print(organization, title, description)
    #         success, message = ClauseService.create_clause(
    #             organization, title, description)

    #         if success:
    #             # Redirige a la lista de cláusulas
    #             return redirect('clause_list')
    #         else:
    #             return render(request, 'clauses/clause_create.html', {'error': message})

    #     organizations = Organization.objects.all()
    #     return render(request, 'clauses/clause_create.html', {'organizations': organizations})
    def create_clause(request):
        data = dict()
        if request.method == 'POST':
            form = ClauseForm(request.POST)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                # Aquí puedes renderizar la lista actualizada si lo deseas
                # data['html_clause_list'] = render_to_string('clause_list.html', {'clauses': Clause.objects.all()})
            else:
                data['form_is_valid'] = False
        else:
            form = ClauseForm()
        context = {'form': form}
        data['html_form'] = render_to_string('components/forms/form_clause.html', context, request=request)
        return JsonResponse(data)

    @login_required
    @staticmethod
    def update_clause(request, clause_id):
        clause = Clause.objects.get(id=clause_id)

        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            if not title or not description:
                return render(request, 'clauses/update_clause.html', {
                    'clause': clause,
                    'error': 'Todos los campos son obligatorios'
                })

            success, message = ClauseService.update_clause(
                clause_id, title, description)

            if success:
                # Redirige a la lista de cláusulas
                return redirect('clause_list')
            else:
                return render(request, 'clauses/update_clause.html', {'clause': clause, 'error': message})

        return render(request, 'clauses/update_clause.html', {'clause': clause})

    @login_required
    @staticmethod
    def delete_clause(request, clause_id):
        clause = Clause.objects.get(id=clause_id)
        if request.method == 'POST':
            success = ClauseService.delete_clause(clause_id)
            if success:
                # Redirige a la lista de cláusulas
                return redirect('clause_list')
            else:
                return HttpResponse('No se pudo eliminar la cláusula', status=400)

        return render(request, 'clauses/delete_clause.html', {'clause': clause})
