from rest_framework.viewsets import generics
from rest_framework.views import Response
from accounts.API.serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.request import Request


class UserRegister(generics.CreateAPIView):
    """
    API endpoint for registering a new user.

    This class-based view allows anyone to create a new user account. It performs basic
    validation, including checking for the uniqueness of the username and securely hashing
    the user's password before storing it in the database.

    **Methods**:
    - POST: Registers a new user with the provided username and password.

    **Fields**:
    - `username` (string, required): The desired username for the new user, must be unique.
    - `password` (string, required): The password for the user, which will be hashed before saving.

    **Response Codes**:
    - 201 Created: User was successfully created.
    - 400 Bad Request: Validation failed due to one of the following reasons:
        - The username is already taken.
        - The password was not provided.

    **Notes**:
    - This endpoint is accessible to any user, including unauthenticated users (`AllowAny` permission class).
    - Passwords are hashed using Django's `make_password` function before being saved.
    """

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'The user with the given login already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()

        password = mutable_data.get('password')
        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(password)
        mutable_data['password'] = hashed_password

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
