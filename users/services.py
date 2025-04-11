from django.contrib.auth.models import User
from .models import ExtendedUser, Organization, TypeIdentification
from django.db import transaction


class UserService:
    def get_users(self):
        return ExtendedUser.objects.select_related('user', 'organization', 'type_identification').all()

    def get_user(self, user_id):
        return ExtendedUser.objects.select_related('user').get(user__id=user_id)

    @staticmethod
    def create_user(user_data):
        try:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )

            extended_user = ExtendedUser.objects.create(
                user=user,
                phone_number=user_data['phone_number'],
                identification_number=user_data['identification_number'],
                birth_date=user_data['birth_date'],
                address=user_data['address'],
                type_identification=TypeIdentification.objects.get(
                    id=user_data['type_identification_id']),
                organization=Organization.objects.get(
                    id=user_data['organization_id'])
            )

            return True, "Usuario creado exitosamente"
        except Exception as e:
            return False, str(e)


def update_user(self, user_id, user_data, extended_data):
    try:
        with transaction.atomic():  # Transacción para asegurar integridad
            # Actualizar User
            user = User.objects.get(id=user_id)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

            # Actualizar ExtendedUser
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
