from trainings.API.serializers import TrainingPlanExerciseInfoSerializer
from trainings.models import TrainingPlanExerciseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet

class TrainingPlanExerciseInfoViewSet(ModelViewSet):
    """
    A viewset for managing exercise information within a training plan. This allows authenticated users
    to retrieve, update, and delete exercise details related to a specific training plan.

    **Permissions**:
    - Only authenticated users can access and manage training plan exercise information.

    **Authentication**:
    - JWT authentication is required to verify user identity.

    **Functionality**:
    - Users can manage exercise information within their training plans.
    - The exercise information is retrieved based on the provided exercise info ID.
    """

    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingPlanExerciseInfo:
        """
        Retrieves a specific exercise information record from a training plan based on the provided ID.
        Raises an error if the record does not exist.
        """

        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info
