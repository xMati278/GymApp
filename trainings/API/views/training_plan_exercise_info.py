from rest_framework.viewsets import generics
from trainings.API.serializers import TrainingPlanExerciseInfoSerializer
from trainings.models import TrainingPlanExerciseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateTrainingPlanExerciseInfo(generics.CreateAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReadTrainingPlanExerciseInfo(generics.ListAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingPlanExerciseInfo:
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class UpdateTrainingPlanExerciseInfo(generics.UpdateAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class DestroyTrainingPlanExerciseInfo(generics.DestroyAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info