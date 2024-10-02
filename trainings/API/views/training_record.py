from trainings.API.serializers import TrainingRecordSerializer
from trainings.models import TrainingRecord
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

class TrainingRecordViewSet(ModelViewSet):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
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
        user_id = self.request.user.id
        return TrainingRecord.objects.filter(user=user_id)


# class ListCreateTrainingRecordsApiView(ListCreateAPIView):
#     queryset = TrainingRecord.objects.all()
#     serializer_class = TrainingRecordSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_object(self) -> TrainingRecord:
#         user = self.kwargs.get('user')
#         request_user = self.request.user.id
#
#         if request_user != user:
#             self.permission_denied(self.request)
#
#         return TrainingRecord.objects.get(user=user)
#
#
# class UpdateDestroyTrainingRecordApiView(RetrieveUpdateDestroyAPIView):
#     queryset = TrainingRecord.objects.all()
#     serializer_class = TrainingRecordSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_object(self) -> TrainingRecord:
#         user = self.request.user.id
#         record_id = self.kwargs.get('pk')
#
#         try:
#             record = TrainingRecord.objects.get(pk=record_id, user=user)
#             return record
#
#         except TrainingRecord.DoesNotExist:
#             self.permission_denied(self.request)