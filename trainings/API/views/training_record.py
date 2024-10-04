from trainings.API.serializers import TrainingRecordSerializer
from trainings.models import TrainingRecord
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

class TrainingRecordViewSet(ModelViewSet):
    """
    A viewset for managing training records. This allows authenticated users to create, retrieve,
    update, and delete their own training records.

    **Permissions**:
    - Only authenticated users can access and manage their training records.
    - Users cannot access records belonging to other users.

    **Authentication**:
    - JWT authentication is required to verify user identity.

    **Functionality**:
    - Users can manage their own training records.
    - The viewset checks for proper permissions when accessing specific records, ensuring that
      users can only view and modify their own records.
    """

    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Retrieves a specific training record for the authenticated user.
        - Checks if the record belongs to the authenticated user.
        - Raises a PermissionDenied error if the user tries to access a record that is not theirs or
          if the record does not exist.
        """

        user_id = self.request.user.id
        url_user_id = self.kwargs.get('user')
        record_id = self.kwargs.get('pk')

        if url_user_id and user_id != int(url_user_id):
            raise PermissionDenied("You do not have permission to access this record.")

        if record_id:
            try:
                return TrainingRecord.objects.get(pk=record_id, user=user_id)
            except TrainingRecord.DoesNotExist:
                raise PermissionDenied("Record not found or you do not have permission to access it.")

        return super().get_object()

    def get_queryset(self):
        """
        Returns the queryset of training records specific to the authenticated user.
        """

        user_id = self.request.user.id
        return TrainingRecord.objects.filter(user=user_id)
