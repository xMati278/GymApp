from rest_framework.viewsets import generics
from trainings.API.serializers import TrainingRecordSerializer
from trainings.models import TrainingRecord
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateTrainingRecord(generics.CreateAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReadTrainingRecord(generics.ListAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.kwargs.get('user')
        request_user = self.request.user.id

        if request_user != user:
            self.permission_denied(self.request)

        return TrainingRecord.objects.get(user=user)


class UpdateTrainingRecord(generics.UpdateAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.request.user.id
        record_id = self.kwargs.get('pk')

        try:
            record = TrainingRecord.objects.get(pk=record_id, user=user)
            return record

        except TrainingRecord.DoesNotExist:
            self.permission_denied(self.request)


class DestroyTrainingRecord(generics.DestroyAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.request.user.id
        record_id = self.kwargs.get('pk')
        try:
            training = TrainingRecord.objects.get(pk=record_id, user=user)
            return training
        except TrainingRecord.DoesNotExist:
            self.permission_denied(self.request)