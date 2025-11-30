from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    
    # You will need to handle extra fields from Signup.tsx (e.g., role, farmLocation)
    # For now, let's include the fields that map directly to the User model.
    # BEST PRACTICE: Use a Custom User Model to natively include fields like 'mobileNumber' and 'role'.

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # This uses Django's built-in function to correctly hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims/user info to the token payload if needed
        token['username'] = user.username
        # token['role'] = user.role # If you have a custom User model

        return token

    def validate(self, attrs):
        # The parent validation handles authentication (username/password check)
        data = super().validate(attrs)

        # Include user details in the login response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # 'role': self.user.role # Include role here
        }
        
        return data