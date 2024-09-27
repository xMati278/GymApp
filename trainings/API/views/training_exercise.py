from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from trainings.API.serializers import TrainingExerciseSerializer
from trainings.models import TrainingPlanExerciseInfo, TrainingExercise
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import generics


class ListCreateTrainingExercisesApiView(ListCreateAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class UpdateDestroyTrainingExerciseApiView(RetrieveUpdateDestroyAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]