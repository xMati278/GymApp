from rest_framework.views import Response
from rest_framework.generics import ListAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from trainings.API.serializers import ExercisesSerializer, BodyPartSerializer
from trainings.models import Exercise, BodyPart
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


class GetAllBodyParts(ListAPIView):
    serializer_class = BodyPartSerializer
    queryset = BodyPart.objects.all()

class ExerciseViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        exercise_type = self.request.query_params.get(key='type', default='public')

        if exercise_type == 'private':
            user = self.request.user
            return Exercise.objects.filter(user=user)

        else:
            return Exercise.objects.filter(public=True)

    def get_object(self) -> Exercise:
        user = self.request.user.id
        exercise_id = self.kwargs.get('pk')

        try:
            exercise = Exercise.objects.get(pk=exercise_id, user=user)
            return exercise

        except Exercise.DoesNotExist:
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

    def get_permissions(self):
        if self.request.method == "POST":

            return [IsAuthenticated()]

        else:

            return [AllowAny()]
