from rest_framework.views import Response
from trainings.API.serializers import UserTrainingPlansSerializer
from trainings.models import UserTrainingPlans
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from typing import Any
from rest_framework.request import Request

class UserTrainingPlansViewSet(ModelViewSet):
    """
    A viewset for managing user training plans. This allows authenticated users to create, retrieve,
    update, and delete their own training plans.

    **Permissions**:
    - Only authenticated users can access and manage their own training plans.

    **Authentication**:
    - JWT authentication is required to verify user identity.

    **Functionality**:
    - Users can manage their own training plans.
    - Only the owner of a training plan can view, modify, or delete it.
    - The viewset ensures proper validation and permission checks during creation and access.
    """

    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self) -> UserTrainingPlans:
        """
        Returns the training plans specific to the authenticated user.
        """

        user = self.request.user
        return UserTrainingPlans.objects.filter(user=user)

    def get_object(self) -> UserTrainingPlans:
        """
        Retrieves a specific training plan for the authenticated user.
        Raises a permission error if the plan does not exist or does not belong to the user.
        """

        user = self.request.user.id
        plan_id = self.kwargs.get('pk')

        try:
            training_plan = UserTrainingPlans.objects.get(pk=plan_id, user=user)
            return training_plan
        except UserTrainingPlans.DoesNotExist:
            self.permission_denied(self.request)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Creates a new training plan for the authenticated user.
        The user is automatically associated with the training plan.
        """

        mutable_data = request.data.copy()
        mutable_data['user'] = self.request.user.id

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
