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
from .views import ClauseView, AreaView
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
    
]
