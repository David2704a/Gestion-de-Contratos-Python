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

# =============================================
# INICIO DE SESIÓN
# =============================================


@login_required
def home(request):
    user_groups = request.user.groups.all()
    return render(request, 'home.html', {
        'request': request,
        'user_groups': user_groups, })


def cerrar_ses(request):
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

    @staticmethod
    def list_users(request):
        users = ExtendedUser.objects.select_related(
            'user', 'organization', 'type_identification').all()
        return render(request, 'users/list_users.html', {'users': users})

    @staticmethod
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

            if success:
                return redirect('user_list')
            else:
                return render(request, 'users/create_user.html', {'error': message})

        organizations = Organization.objects.all()
        identifications = TypeIdentification.objects.all()

        return render(request, 'users/create_user.html', {
            'organizations': organizations,
            'identifications': identifications
        })

    @staticmethod
    def edit_user(self, request, user_id):
        user = self.user_service.get_user(user_id)

        if request.method == 'POST':
            user_data = {
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
            }
            extended_data = {
                'phone_number': request.POST.get('phone_number'),
                'identification_number': request.POST.get('identification_number'),
                'birth_date': request.POST.get('birth_date'),
                'address': request.POST.get('address'),
                'type_identification_id': request.POST.get('type_identification_id'),
                'organization_id': request.POST.get('organization_id'),
            }
            self.user_service.update_user(user_id, user_data, extended_data)
            return redirect('list_users')

        organizations = Organization.objects.all()
        identifications = TypeIdentification.objects.all()

        return render(request, 'users/edit_user.html', {
            'user': user.user,
            'extended_user': user,
            'organizations': organizations,
            'identifications': identifications
        })
