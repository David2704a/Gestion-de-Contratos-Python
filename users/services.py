from django.contrib.auth.models import User
from .models import ExtendedUser, Organization, TypeIdentification
from django.db import transaction
from .repositories import UserRepository

class UserService:
    def get_users(self):
        return ExtendedUser.objects.select_related('user', 'organization', 'type_identification').all()

    def get_user(self, user_id):
        return ExtendedUser.objects.select_related('user').get(user__id=user_id)

    @staticmethod
    def create_user(user_data):
        try:
            with transaction.atomic():
                user = UserRepository.create_user(user_data)
                UserRepository.create_extended_user(user, user_data)
            return True, "Usuario creado exitosamente"
        except Exception as e:
            return False, f"Error al crear el usuario: {str(e)}"

    def update_user(self, user_id, user_data, extended_data):
        try:
            with transaction.atomic():  
                
                user = User.objects.get(id=user_id)
                user.username = user_data.get('username', user.username)
                user.email = user_data.get('email', user.email)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.save()

                extended_user = ExtendedUser.objects.get(user=user)
                extended_user.phone_number = extended_data.get(
                    'phone_number', extended_user.phone_number)
                extended_user.identification_number = extended_data.get(
                    'identification_number', extended_user.identification_number)
                extended_user.birth_date = extended_data.get(
                    'birth_date', extended_user.birth_date)
                extended_user.address = extended_data.get(
                    'address', extended_user.address)

                if extended_data.get('type_identification_id'):
                    extended_user.type_identification_id = extended_data['type_identification_id']

                if extended_data.get('organization_id'):
                    extended_user.organization_id = extended_data['organization_id']

                extended_user.save()

                return True, "Usuario actualizado correctamente"

        except User.DoesNotExist:
            return False, "El usuario no existe"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
