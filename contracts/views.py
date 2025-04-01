from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .services import (
    OrganizationService, ClauseService, UserService, ContractService,
    TypeContractService, AreaService, PostService
)

# 🏢 ORGANIZATIONS
def organization_list(request):
    organizations = OrganizationService.get_organizations()
    return render(request, 'organizations/list.html', {'organizations': organizations})

def create_organization(request):
    if request.method == 'POST':
        data = request.POST
        OrganizationService.create_organization(data)
        return redirect('organization_list')
    return render(request, 'organizations/create.html')

def edit_organization(request, org_id):
    organization = get_object_or_404(OrganizationService.get_organization, org_id)
    if request.method == 'POST':
        data = request.POST
        OrganizationService.edit_organization(org_id, data)
        return redirect('organization_list')
    return render(request, 'organizations/edit.html', {'organization': organization})

# 📜 CLAUSES
def clause_list(request):
    clauses = ClauseService.get_clauses()
    return render(request, 'clauses/list.html', {'clauses': clauses})

def create_clause(request):
    if request.method == 'POST':
        data = request.POST
        ClauseService.create_clause(data)
        return redirect('clause_list')
    return render(request, 'clauses/create.html')

def edit_clause(request, clause_id):
    clause = get_object_or_404(ClauseService.get_clause, clause_id)
    if request.method == 'POST':
        data = request.POST
        ClauseService.edit_clause(clause_id, data)
        return redirect('clause_list')
    return render(request, 'clauses/edit.html', {'clause': clause})

# 👥 USERS
def user_list(request):
    users = UserService.get_users()
    return render(request, 'users/list.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        data = request.POST
        UserService.create_user(data)
        return redirect('user_list')
    return render(request, 'users/create.html')

def edit_user(request, user_id):
    user = get_object_or_404(UserService.get_user, user_id)
    if request.method == 'POST':
        data = request.POST
        UserService.edit_user(user_id, data)
        return redirect('user_list')
    return render(request, 'users/edit.html', {'user': user})

# 📄 CONTRACTS
def contract_list(request):
    contracts = ContractService.get_contracts()
    return render(request, 'contracts/list.html', {'contracts': contracts})

def create_contract(request):
    if request.method == 'POST':
        data = request.POST
        ContractService.create_contract(data)
        return redirect('contract_list')
    return render(request, 'contracts/create.html')

def edit_contract(request, contract_id):
    contract = get_object_or_404(ContractService.get_contract, contract_id)
    if request.method == 'POST':
        data = request.POST
        ContractService.edit_contract(contract_id, data)
        return redirect('contract_list')
    return render(request, 'contracts/edit.html', {'contract': contract})

def approve_contract(request, contract_id):
    ContractService.approve_contract(contract_id)
    return redirect('contract_list')

def contracts_to_finalize(request):
    contracts = ContractService.obtain_contracts_to_finalize()
    return render(request, 'contracts/finalize.html', {'contracts': contracts})

# 📂 TYPE CONTRACTS
def type_contract_list(request):
    type_contracts = TypeContractService.get_type_contract()
    return render(request, 'type_contracts/list.html', {'type_contracts': type_contracts})

def create_type_contract(request):
    if request.method == 'POST':
        data = request.POST
        TypeContractService.create_type_contract(data)
        return redirect('type_contract_list')
    return render(request, 'type_contracts/create.html')

# 📌 AREAS
def area_list(request):
    areas = AreaService.get_areas()
    return render(request, 'areas/list.html', {'areas': areas})

def create_area(request):
    if request.method == 'POST':
        data = request.POST
        AreaService.create_area(data)
        return redirect('area_list')
    return render(request, 'areas/create.html')

# 📍 POSTS
def post_list(request):
    posts = PostService.get_posts()
    return render(request, 'posts/list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        data = request.POST
        PostService.create_post(data)
        return redirect('post_list')
    return render(request, 'posts/create.html')
