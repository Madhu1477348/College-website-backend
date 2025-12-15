from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # We need to ensure 'username' key exists because TokenObtainPairSerializer might check it
        # However, we are setting username_field = 'email', so it might check 'email' fromattrs.
        
        # But wait, standard TokenObtainPair calls authenticate which eventually calls our EmailBackend.
        # Our EmailBackend expects 'username' arg to be the email.
        # The parent validate() method pulls self.username_field from attrs.
        # Since we set username_field = 'email', it will pull attrs['email'].
        # Then it calls authenticate(request=..., **{self.username_field: ..., 'password': ...})
        # So it calls authenticate(email=...)
        # Our EmailBackend.authenticate(..., username=None, password=..., **kwargs) has logic:
        # if username is None: username = kwargs.get('email')
        # So this should work perfectly!
        
        data = super().validate(attrs)
        return data
