from rest_framework.viewsets import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from .calculators import Calculators
from .serializers import BodyPartSerializer, Calculate1RMSerializer, PointsCalculatorSerializer,\
    CalculateTotalSerializer, CalculatorResultSerializer, TotalCalculatorResultSerializer, GetExercisesSerializer,\
    GetUserTrainingPlansSerializer, CreatePrivateExerciseSerializer,\
    DeleteExerciseSerializer
from trainings.models import BodyPart, Exercise, UserTrainingPlans


class Calculate1RM(APIView):
    """
    Validate, calculates and returns one rep max weight for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs) -> JsonResponse:
        serializer = Calculate1RMSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_1rm_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateWilks(APIView):
    """
        Validate, calculates and returns wilks points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_wilks_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateDots(APIView):
    """
        Validate, calculates and returns dots points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_dots_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateIpfGl(APIView):
    """
        Validate, calculates and returns dots points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_ipf_gl_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateTotal(APIView):
    """
        Validate, calculates and returns total data for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = CalculateTotalSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.total_logic(**serializer.validated_data)
            total_result_serializer = TotalCalculatorResultSerializer(data=result)

            if total_result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=total_result_serializer.validated_data)


#TODO od tego momentu brak testów do api
class GetAllBodyParts(generics.ListAPIView):
    serializer_class = BodyPartSerializer
    queryset = BodyPart.objects.all()


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


class ReadPublicExercises(generics.ListAPIView):
    serializer_class = ExercisesSerializer
    queryset = Exercise.objects.filter(public=True)


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

class GetPublicExercises(generics.ListAPIView):
    serializer_class = GetExercisesSerializer
    queryset = Exercise.objects.filter(public=True)


class GetPrivateExercises(generics.ListAPIView): #TODO walidacja

    serializer_class = GetExercisesSerializer

    def get_queryset(self):
        queryset = Exercise.objects.filter(user=self.request.user, public=False)

        return queryset


class GetUserTrainingPlans(generics.ListAPIView): #TODO walidacja
    serializer_class = GetUserTrainingPlansSerializer

    def get_queryset(self):
        queryset = UserTrainingPlans.objects.filter(user=self.request.user)

        return queryset
