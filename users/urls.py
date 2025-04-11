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
from .views import UserView
from .views import home


urlpatterns = [
    # HOME
    
    # USERS
    path('list/', UserView.users_lists, name='users_lists'),
    path('create/', UserView.create_user, name='create_user'),
    path('edit/<int:user_id>/', UserView.edit_user, name='edit_user'),
]