from django.contrib.auth.models import User
from .models import ExtendedUser, Organization, TypeIdentification

class UserRepository:

    @staticmethod
    def create_user(user_data):
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password']
        )
        return user

    @staticmethod
    def create_extended_user(user, user_data):
        extended_user = ExtendedUser.objects.create(
            user=user,
            phone_number=user_data['phone_number'],
            identification_number=user_data['identification_number'],
            birth_date=user_data['birth_date'],
            address=user_data['address'],
            type_identification=TypeIdentification.objects.get(id=user_data['type_identification_id']),
            organization=Organization.objects.get(id=user_data['organization_id']),
        )
        return extended_user