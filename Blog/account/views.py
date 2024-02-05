from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status

# Registration logic for new user
class RegisterView(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            data = request.data
            # Validate and serialize the registration data
            serializer = RegisterSerializer(data=data)

            # Check if the data is valid
            if not serializer.is_valid():
                # Return an error response with validation errors
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Registration credentials invalid"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            
            # Save the user in the database
            serializer.save()

            # Return a success response
            return Response(
                {
                    'data': {},
                    'message': "Registration Successful"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Handle any exceptions that may occur during registration
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Exception occurred while registration"
                }, status=status.HTTP_400_BAD_REQUEST
            )


# Log in logic for an already existing user
class LoginView(APIView):

    def post(self, request):
        try:
            # Extract data from the request
            data = request.data
            # Validate and serialize the login data
            serializer = LoginSerializer(data=data)

            # Check if the data is valid
            if not serializer.is_valid():
                # Return an error response with validation errors
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Credentials invalid"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            # Get the JWT token and other relevant details
            response = serializer.get_jwt_token(serializer.data)
            
            # Return a success response with the JWT token
            return Response(response, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            # Handle any exceptions that may occur during login
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Exception occurred while login"
                }, status=status.HTTP_400_BAD_REQUEST
            )
