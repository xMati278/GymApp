from rest_framework.viewsets import generics
from rest_framework.views import Response
from trainings.API.serializers import ExercisesSerializer, BodyPartSerializer
from trainings.models import Exercise, BodyPart
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


class GetAllBodyParts(generics.ListAPIView):
    serializer_class = BodyPartSerializer
    queryset = BodyPart.objects.all()

class ReadPublicExercises(generics.ListAPIView):
    serializer_class = ExercisesSerializer
    queryset = Exercise.objects.filter(public=True)


class CreatePrivateExercise(generics.CreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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


class ReadPrivateExercises(generics.ListAPIView):
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Exercise.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# class ListCreatePrivateExercisesAPIView(generics.ListCreateAPIView):
#     serializer_class = ExercisesSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Exercise.objects.filter(user=user)
#
#     def create(self, request, *args, **kwargs):
#         mutable_data = request.data.copy()
#         mutable_data['user'] = self.request.user.id
#
#         serializer = self.get_serializer(data=mutable_data)
#         if serializer.is_valid():
#             serializer.save()
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePrivateExercise(generics.UpdateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> Exercise:
        user = self.request.user.id
        exercise_id = self.kwargs.get('pk')

        try:
            exercise = Exercise.objects.get(pk=exercise_id, user=user)
            return exercise

        except Exercise.DoesNotExist:
            self.permission_denied(self.request)


class DeletePrivateExercise(generics.DestroyAPIView):
    serializer_class = ExercisesSerializer
    queryset = Exercise.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> Exercise:
        user = self.request.user.id
        exercise_id = self.kwargs.get('pk')

        try:
            exercise = Exercise.objects.get(pk=exercise_id, user=user)
            return exercise

        except Exercise.DoesNotExist:
            self.permission_denied(self.request)