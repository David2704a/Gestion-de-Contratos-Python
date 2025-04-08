from django.contrib.auth.models import User
from .models import ExtendedUser, Organization, TypeIdentification

class UserService:
    def get_users(self):
        return ExtendedUser.objects.select_related('user', 'organization', 'type_identification').all()

    def get_user(self, user_id):
        return ExtendedUser.objects.select_related('user').get(user__id=user_id)

    def create_user(self, user_data, extended_data):
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password']
        )
        extended_user = ExtendedUser.objects.create(
            user=user,
            phone_number=extended_data['phone_number'],
            identification_number=extended_data['identification_number'],
            birth_date=extended_data['birth_date'],
            address=extended_data['address'],
            type_identification=TypeIdentification.objects.get(id=extended_data['type_identification_id']),
            organization=Organization.objects.get(id=extended_data['organization_id'])
        )
        return extended_user

    def update_user(self, user_id, user_data, extended_data):
        user = User.objects.get(id=user_id)
        extended_user = ExtendedUser.objects.get(user=user)

        user.username = user_data['username']
        user.email = user_data['email']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.save()

        extended_user.phone_number = extended_data['phone_number']
        extended_user.identification_number = extended_data['identification_number']
        extended_user.birth_date = extended_data['birth_date']
        extended_user.address = extended_data['address']
        extended_user.type_identification_id = extended_data['type_identification_id']
        extended_user.organization_id = extended_data['organization_id']
        extended_user.save()

        return extended_user