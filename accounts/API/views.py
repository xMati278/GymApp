from rest_framework.viewsets import generics
from rest_framework.views import Response
from accounts.API.serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
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
