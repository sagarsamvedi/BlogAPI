from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status

# Registration logic for new user
class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Registration credentials invalid"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            serializer.save()
            return Response(
                {
                    'data': {},
                    'message': "Registration Successful"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Exception occured while registration"
                }, status=status.HTTP_400_BAD_REQUEST
            )


# Log in logic for already exist user
class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "credentials invalid"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Exception occured while log in"
                }, status=status.HTTP_400_BAD_REQUEST
            )