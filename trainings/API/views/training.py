from rest_framework.views import Response
from trainings.API.serializers import TrainingSerializer
from trainings.models import Training
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class TrainingViewSet(ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Training.objects.filter(user=user)

    def get_object(self) -> Training:
        user = self.request.user.id
        training_id = self.kwargs.get('pk')

        try:
            training = Training.objects.get(pk=training_id, user=user)
            return training
        except Training.DoesNotExist:
            self.permission_denied(self.request)

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['user'] = self.request.user.id

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
