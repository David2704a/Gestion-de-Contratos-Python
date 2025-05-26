from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .services import UserService
from contracts.models import Organization
from .models import TypeIdentification
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ExtendedUser
from django.contrib.auth.models import User
from django.contrib import messages


# =============================================
# INICIO DE SESIÓN
# =============================================


@login_required
def home(request):
    user_groups = request.user.groups.all()
    return render(request, 'home.html', {
        'request': request,
        'user_groups': user_groups, })


def logout_view(request):
    logout(request) 
    return redirect('home')


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'request': request,
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect',
                'request': request,
            })
        else:
            login(request, user)
            return redirect('home')


class UserView:
    @login_required
    @staticmethod
    def users_lists(request):
        users = ExtendedUser.objects.select_related(
            'user', 'organization', 'type_identification').all()
        return render(request, 'users/users_lists.html', {'users': users})
    
    @login_required
    def create_user(request):
        if request.method == 'POST':
            data = {
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone_number': request.POST.get('phone_number'),
                'identification_number': request.POST.get('identification_number'),
                'birth_date': request.POST.get('birth_date'),
                'address': request.POST.get('address'),
                'type_identification_id': request.POST.get('type_identification_id'),
                'organization_id': request.POST.get('organization_id'),
            }
    
            success, message = UserService.create_user(data)
    
            return JsonResponse({
                'success': success,
                'message': message
            })
    
        organizations = Organization.objects.all()
        identifications = TypeIdentification.objects.all()
    
        return render(request, 'users/create_user.html', {
            'organizations': organizations,
            'identifications': identifications
        })

    @login_required
    @staticmethod
    def edit_user(request, user_id):

        try:
            extended_user = ExtendedUser.objects.select_related('user').get(user_id=user_id)
            
            if request.method == 'POST':
                
                required_fields = ['username', 'email', 'first_name']
                missing_fields = [field for field in required_fields if not request.POST.get(field)]
                
                if missing_fields:
                    raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
                
                user_data = {
                    'username': request.POST['username'],
                    'email': request.POST['email'],
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST.get('last_name', ''),
                }
                
                extended_data = {
                    'phone_number': request.POST.get('phone_number', ''),
                    'identification_number': request.POST.get('identification_number', ''),
                    'birth_date': request.POST.get('birth_date'),
                    'address': request.POST.get('address', ''),
                    'type_identification_id': request.POST.get('type_identification_id'),
                    'organization_id': request.POST.get('organization_id'),
                }
                
                success, message = UserService().update_user(user_id, user_data, extended_data)
                if success:
                    messages.success(request, message)
                    return redirect('users_lists')
                else:
                    raise Exception(message)
        
        except ExtendedUser.DoesNotExist:
            messages.error(request, "El usuario no existe")
            return redirect('users_lists')
        except ValueError as e:
            messages.warning(request, str(e))
        except Exception as e:
            messages.error(request, f"Error al actualizar usuario: {str(e)}")
        
        # GET request o fallo en POST
        organizations = Organization.objects.all()
        identifications = TypeIdentification.objects.all()
        is_superadmin = request.user.groups.filter(name='superAdministrators').exists()
        return render(request, 'users/edit_user.html', {
            'user': extended_user.user,
            'extended_user': extended_user,
            'organizations': organizations,
            'identifications': identifications,
            'selected_org': extended_user.organization_id,
            'selected_id_type': extended_user.type_identification_id,
            'is_superadmin': is_superadmin  # 👈 Aquí
        })