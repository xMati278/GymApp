from trainings.API.serializers import TrainingExerciseSerializer
from trainings.models import TrainingPlanExerciseInfo, TrainingExercise
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound

class TrainingExerciseViewSet(ModelViewSet):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        try:
            exercise_info = TrainingExercise.objects.get(pk=exercise_info_id)
        except TrainingPlanExerciseInfo.DoesNotExist:
            raise NotFound(f"TrainingExercise with id {exercise_info_id} does not exist.")

        return exercise_info
