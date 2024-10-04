from rest_framework.views import Response
from trainings.API.serializers import TrainingSerializer
from trainings.models import Training
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from typing import Any
from rest_framework.request import Request


class TrainingViewSet(ModelViewSet):
    """
    A viewset for managing training sessions. This allows authenticated users to create, retrieve,
    update, and delete their own training sessions.

    **Permissions**:
    - Only authenticated users can access and manage their own training data.

    **Authentication**:
    - JWT authentication is required to verify user identity.

    **Functionality**:
    - Users can only view and modify their own training sessions.
    - The viewset handles creation, retrieval, and validation of training data.
    """

    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self) -> Training:
        """
        Returns the training sessions specific to the authenticated user.
        """

        user = self.request.user
        return Training.objects.filter(user=user)

    def get_object(self) -> Training:
        """
        Retrieves a specific training session object for the authenticated user.
        Raises a permission error if the session does not exist or does not belong to the user.
        """

        user = self.request.user.id
        training_id = self.kwargs.get('pk')

        try:
            training = Training.objects.get(pk=training_id, user=user)
            return training
        except Training.DoesNotExist:
            self.permission_denied(self.request)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Creates a new training session for the authenticated user.
        The user is automatically associated with the training session.
        """

        mutable_data = request.data.copy()
        mutable_data['user'] = self.request.user.id

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
