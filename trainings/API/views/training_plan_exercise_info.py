from trainings.API.serializers import TrainingPlanExerciseInfoSerializer
from trainings.models import TrainingPlanExerciseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet

class TrainingPlanExerciseInfoViewSet(ModelViewSet):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingPlanExerciseInfo:
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info
