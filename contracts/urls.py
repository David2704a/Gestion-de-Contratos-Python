from django.urls import path
# from .views import (
#     organization_list, create_organization, edit_organization,
#     clause_list, create_clause, edit_clause,
#     user_list, create_user, edit_user,
#     contract_list, create_contract, edit_contract, approve_contract, contracts_to_finalize,
#     type_contract_list, create_type_contract,
#     area_list, create_area,
#     post_list, create_post
# )
from .views import ClauseView, AreaView, TypeContractView, PostView, ContractView
urlpatterns = [
    
    #CLÁUSULAS
    path('clause_list/', ClauseView.clauses_list, name='clause_list'),
    path('clauses/create/', ClauseView.create_clause, name='create_clause'),
    path('clauses/<int:clause_id>/update/', ClauseView.update_clause, name='update_clause'),
    path('clauses/<int:clause_id>/delete/', ClauseView.delete_clause, name='delete_clause'),
    
    #ÁREAS
    path('area_list/', AreaView.areas_list, name='areas_list'),
    path('areas/create/', AreaView.create_area, name='create_area'),
    path('areas/<int:area_id>/delete/', AreaView.delete_area, name='delete_area'),
    path('areas/<int:area_id>/update/', AreaView.update_area, name='update_area'),
    
    #TIPOS DE CONTRATO
    
    path('typeContract_list/', TypeContractView.typeC_list, name='typeC_list'),
    path('typeContracts/create/', TypeContractView.create_typeC, name='create_type_contract'),
    path('typeContracts/<int:typecon_id>/delete/', TypeContractView.delete_typeC, name='delete_type_contract'),
    path('typeContracts/<int:typecon_id>/update/', TypeContractView.update_typeC, name='update_type_contract'),
    
    #CARGOS
    
    path('post_list/', PostView.posts_list, name='post_list'),
    path('posts/create/', PostView.create_post, name='create_post'),
    path('posts/<int:post_id>/delete/', PostView.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update/', PostView.update_post, name='update_post'),
    
    #CARGOS
    
    path('contracts_list/', ContractView.contracts_list, name='contracts_list'),
    path('contracts_create/', ContractView.contracts_create, name='contracts_create'),
    path('contracts/<int:contract_id>/pdf/', ContractView.contract_view_pdf, name='contract_pdf_view'),
    
]
