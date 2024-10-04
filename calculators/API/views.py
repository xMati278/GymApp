from django.http import JsonResponse
from rest_framework.views import APIView
from calculators.API.calculators import Calculators
from calculators.API.serializers import (Calculate1RMSerializer, CalculatorResultSerializer, CalculateTotalSerializer,
                                       PointsCalculatorSerializer, TotalCalculatorResultSerializer)
from rest_framework.request import Request

class Calculate1RM(APIView):
    """
    Validates the input data and calculates the one-rep max (1RM) based on the provided information.
    """

    @staticmethod
    def get(request: Request, *args, **kwargs) -> JsonResponse:
        serializer = Calculate1RMSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_1rm_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateWilks(APIView):
    """
    Validates the input data and calculates Wilks points based on the provided information.
    """

    @staticmethod
    def get(request: Request, *args, **kwargs) -> JsonResponse:
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_wilks_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateDots(APIView):
    """
    Validates the input data and calculates DOTS points based on the provided information.
    """

    @staticmethod
    def get(request: Request, *args, **kwargs) -> JsonResponse:
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_dots_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateIpfGl(APIView):
    """
    Validates the input data and calculates IPF GL points based on the provided information.
    """

    @staticmethod
    def get(request: Request, *args, **kwargs) -> JsonResponse:
        serializer = PointsCalculatorSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.calculate_ipf_gl_logic(**serializer.validated_data)
            result_serializer = CalculatorResultSerializer(data=result)

            if result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=result_serializer.validated_data)


class CalculateTotal(APIView):
    """
    Validates the input data and calculates the total result based on the provided information.
    """

    @staticmethod
    def get(request: Request, *args, **kwargs) -> JsonResponse:
        serializer = CalculateTotalSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            result = Calculators.total_logic(**serializer.validated_data)
            total_result_serializer = TotalCalculatorResultSerializer(data=result)

            if total_result_serializer.is_valid(raise_exception=True):
                return JsonResponse(data=total_result_serializer.validated_data)
