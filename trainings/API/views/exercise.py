from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from trainings.API.serializers import ExercisesSerializer, BodyPartSerializer
from trainings.models import Exercise, BodyPart
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from typing import Any, Dict, Optional


class GetAllBodyParts(ListAPIView):
    """
    Retrieves and returns a list of all available body parts.
    """

    serializer_class = BodyPartSerializer
    queryset = BodyPart.objects.all()

class ExerciseViewSet(ModelViewSet):
    """
    A viewset for managing exercises, allowing creation, retrieval, updating, and deletion of exercises.

    - The view supports both public and private exercises.
    - Authenticated users can create, view, and manage their own private exercises.
    - Public exercises are accessible to all users.

    **Permissions**:
    - Only authenticated users can create exercises.
    - Public exercises can be viewed by any user.

    **Authentication**:
    - JWT authentication is used to verify the identity of users when necessary.
    """

    queryset = Exercise.objects.all()
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self) -> Exercise:
        """
        Returns the appropriate queryset based on the type of exercise (public or private).
        """

        exercise_type = self.request.query_params.get(key='type', default='public')

        if exercise_type == 'private':
            user = self.request.user
            return Exercise.objects.filter(user=user)

        else:
            return Exercise.objects.filter(public=True)

    def get_object(self) -> Exercise:
        """
        Retrieves a specific exercise object for the authenticated user.
        Raises a permission error if the exercise does not exist.
        """

        user = self.request.user.id
        exercise_id = self.kwargs.get('pk')

        try:
            exercise = Exercise.objects.get(pk=exercise_id, user=user)
            return exercise

        except Exercise.DoesNotExist:
            self.permission_denied(self.request)

    def create(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Creates a new exercise for the authenticated user.
        The user is automatically assigned to the exercise being created.
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

    def get_permissions(self) -> list:
        """
        Returns the appropriate permission classes based on the HTTP method.
        Only authenticated users can create exercises, while other actions may allow anonymous access.
        """

        if self.request.method == "POST":

            return [IsAuthenticated()]

        else:

            return [AllowAny()]
