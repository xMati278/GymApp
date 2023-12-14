from rest_framework.viewsets import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .calculators import Calculators
from .serializers import BodyPartSerializer, Calculate1RMSerializer, PointsCalculatorSerializer,\
    CalculateTotalSerializer, GetExercisesSerializer
from trainings.models import BodyPart, Exercise
# Create your views here.


class Calculate1RM(APIView):
    """
    Validate, calculates and returns one rep max weight for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs) -> JsonResponse:
        serializer = Calculate1RMSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        reps = serializer.validated_data.get('reps')
        lifted_weight = serializer.validated_data.get('weight')
        result = Calculators.calculate_1rm_logic(lifted_weight=lifted_weight, reps=reps)

        return JsonResponse(data={'1rm': result}, status=status.HTTP_200_OK)


class CalculateWilks(APIView):
    """
        Validate, calculates and returns wilks points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        is_female = serializer.validated_data.get('female')
        body_weight = serializer.validated_data.get('body')
        lifted_weight = serializer.validated_data.get('lift')

        result = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight,
                                                   lifted_weight=lifted_weight)

        return JsonResponse(data={'wilks': result}, status=status.HTTP_200_OK)


class CalculateDots(APIView):
    """
        Validate, calculates and returns dots points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        is_female = serializer.validated_data.get('female')
        body_weight = serializer.validated_data.get('body')
        lifted_weight = serializer.validated_data.get('lift')

        result = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight,
                                                  lifted_weight=lifted_weight)

        return JsonResponse(data={'dots': result}, status=status.HTTP_200_OK)


class CalculateIpfGl(APIView):
    """
        Validate, calculates and returns dots points for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = PointsCalculatorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        is_female = serializer.validated_data.get('female')
        body_weight = serializer.validated_data.get('body')
        lifted_weight = serializer.validated_data.get('lift')

        result = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight,
                                                    lifted_weight=lifted_weight)

        return JsonResponse(data={'ipf_gl': result}, status=status.HTTP_200_OK)


class CalculateTotal(APIView):
    """
        Validate, calculates and returns total data for the given data.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = CalculateTotalSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        is_female = serializer.validated_data.get('female')
        body_weight = serializer.validated_data.get('body')
        squat_weight = serializer.validated_data.get('sq')
        squat_reps = serializer.validated_data.get('sq_reps')
        bench_weight = serializer.validated_data.get('bp')
        bench_reps = serializer.validated_data.get('bp_reps')
        deadlift_weight = serializer.validated_data.get('dl')
        deadlift_reps = serializer.validated_data.get('dl_reps')

        result = Calculators.total_logic(is_female=is_female, body_weight=body_weight, squat_weight=squat_weight,
                                         squat_reps=squat_reps, bench_weight=bench_weight, bench_reps=bench_reps,
                                         deadlift_weight=deadlift_weight, deadlift_reps=deadlift_reps)

        return JsonResponse(data=result, status=status.HTTP_200_OK)


class GetAllBodyParts(generics.ListAPIView):
    serializer_class = BodyPartSerializer
    queryset = BodyPart.objects.all()


class GetPublicExercises(generics.ListAPIView):
    serializer_class = GetExercisesSerializer
    queryset = Exercise.objects.filter(public=True)


class GetPrivateExercises(generics.ListAPIView):
    serializer_class = GetExercisesSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        queryset = Exercise.objects.filter(user=user, public=False)

        return queryset
