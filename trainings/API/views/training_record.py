from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from trainings.API.serializers import TrainingRecordSerializer
from trainings.models import TrainingRecord
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ListCreateTrainingRecordsApiView(ListCreateAPIView):
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


class UpdateDestroyTrainingRecordApiView(RetrieveUpdateDestroyAPIView):
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