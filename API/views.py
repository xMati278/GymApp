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


class CreatePrivateExercise(generics.CreateAPIView): #TODO to jest niby GET zamiast POST
    queryset = Exercise.objects.all()
    serializer_class = CreatePrivateExerciseSerializer


class DeletePrivateExercise(generics.DestroyAPIView): #TODO a to niby jest GET zamiast DELETE
    queryset = Exercise.objects.all()
    serializer_class = DeleteExerciseSerializer

    def get_queryset(self):
        training_plan = self.request.query_params.get('training_plan')
        return generics.get_object_or_404(Exercise, id=training_plan)


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
