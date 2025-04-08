from django.contrib.auth.models import User

class UserRepository:
    @staticmethod
    def get_users():
        return User.objects.all()

    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_user(data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return user

    @staticmethod
    def edit_user(user_id, data):
        user = User.objects.get(id=user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user