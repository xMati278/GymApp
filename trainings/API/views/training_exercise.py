from trainings.API.serializers import TrainingExerciseSerializer
from trainings.models import TrainingPlanExerciseInfo, TrainingExercise
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound

class TrainingExerciseViewSet(ModelViewSet):
    """
    A viewset for managing training exercises. This allows authenticated users to retrieve, update,
    and delete specific exercises associated with their training sessions.

    **Permissions**:
    - Only authenticated users can access and manage training exercises.

    **Authentication**:
    - JWT authentication is required to verify user identity.

    **Functionality**:
    - Users can manage their training exercises by retrieving, updating, or deleting them.
    - Exercises are fetched based on the provided exercise ID.
    """

    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Retrieves a specific training exercise based on the provided exercise ID.
        Raises a NotFound error if the exercise does not exist.
        """

        exercise_info_id = self.kwargs.get('pk')
        try:
            exercise_info = TrainingExercise.objects.get(pk=exercise_info_id)
        except TrainingPlanExerciseInfo.DoesNotExist:
            raise NotFound(f"TrainingExercise with id {exercise_info_id} does not exist.")

        return exercise_info
