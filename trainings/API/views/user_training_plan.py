from rest_framework.views import Response
from trainings.API.serializers import UserTrainingPlansSerializer
from trainings.models import UserTrainingPlans
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class UserTrainingPlansViewSet(ModelViewSet):
    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserTrainingPlans.objects.filter(user=user)

    def get_object(self) -> UserTrainingPlans:
        user = self.request.user.id
        plan_id = self.kwargs.get('pk')

        try:
            training_plan = UserTrainingPlans.objects.get(pk=plan_id, user=user)
            return training_plan
        except UserTrainingPlans.DoesNotExist:
            self.permission_denied(self.request)

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['user'] = self.request.user.id

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
