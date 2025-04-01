from django.urls import path
from .views import (
    organization_list, create_organization, edit_organization,
    clause_list, create_clause, edit_clause,
    user_list, create_user, edit_user,
    contract_list, create_contract, edit_contract, approve_contract, contracts_to_finalize,
    type_contract_list, create_type_contract,
    area_list, create_area,
    post_list, create_post
)

urlpatterns = [
    # 🏢 Organizations
    path('organizations/', organization_list, name='organization_list'),
    path('organizations/create/', create_organization, name='create_organization'),
    path('organizations/edit/<int:org_id>/',
         edit_organization, name='edit_organization'),

    # 📜 Clauses
    path('clauses/', clause_list, name='clause_list'),
    path('clauses/create/', create_clause, name='create_clause'),
    path('clauses/edit/<int:clause_id>/', edit_clause, name='edit_clause'),

    # 👥 Users
    path('users/', user_list, name='user_list'),
    path('users/create/', create_user, name='create_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),

    # 📄 Contracts
    path('contracts/', contract_list, name='contract_list'),
    path('contracts/create/', create_contract, name='create_contract'),
    path('contracts/edit/<int:contract_id>/',
         edit_contract, name='edit_contract'),
    path('contracts/approve/<int:contract_id>/',
         approve_contract, name='approve_contract'),
    path('contracts/finalize/', contracts_to_finalize,
         name='contracts_to_finalize'),

    # 📂 Type Contracts
    path('type_contracts/', type_contract_list, name='type_contract_list'),
    path('type_contracts/create/', create_type_contract,
         name='create_type_contract'),

    # 📌 Areas
    path('areas/', area_list, name='area_list'),
    path('areas/create/', create_area, name='create_area'),

    # 📍 Posts
    path('posts/', post_list, name='post_list'),
    path('posts/create/', create_post, name='create_post'),
]
