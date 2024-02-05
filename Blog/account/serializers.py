from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Registration Serializer for new user registration
class RegisterSerializer(serializers.Serializer):
    # Define fields required for user registration
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    # Validate the input data
    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken")

        return data

    # Create a new user with validated data
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()

        return validated_data

# Login Serializer for an already existing user with JWT authentication
class LoginSerializer(serializers.Serializer):
    # Define fields required for user login
    username = serializers.CharField()
    password = serializers.CharField()

    # Validate the input data
    def validate(self, data):
        # Check if the username exists
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Account doesn't exist")

        return data

    # Get JWT token for a valid user
    def get_jwt_token(self, data):
        # Authenticate the user with provided username and password
        user = authenticate(
            username=data['username'], password=data['password'])

        # If user is not authenticated, return an error message
        if not user:
            return {
                'data': {},
                'message': 'Invalid credentials'
            }

        # Generate and return the JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'message': 'Login successful',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }
