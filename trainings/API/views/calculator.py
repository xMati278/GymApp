from django.http import JsonResponse
from rest_framework.views import APIView
from trainings.API.calculators import Calculators
from trainings.API.serializers import (Calculate1RMSerializer, CalculatorResultSerializer, CalculateTotalSerializer,
                                       PointsCalculatorSerializer, TotalCalculatorResultSerializer)


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
