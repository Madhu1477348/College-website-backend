from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get('email')
        
        try:
            # Check if the user exists with the given email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            # If user exists, check password
            if user.check_password(password):
                return user
        return None
