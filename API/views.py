from rest_framework.viewsets import generics
from django.http import JsonResponse
from rest_framework.views import APIView, Response
from .calculators import Calculators
from .serializers import BodyPartSerializer, Calculate1RMSerializer, PointsCalculatorSerializer,\
    CalculateTotalSerializer, CalculatorResultSerializer, TotalCalculatorResultSerializer, ExercisesSerializer,\
    UserTrainingPlansSerializer, TrainingSerializer, TrainingRecordSerializer, TrainingPlanExerciseInfoSerializer,\
    TrainingExerciseSerializer, RegistrationSerializer
from trainings.models import BodyPart, Exercise, UserTrainingPlans, Training, TrainingRecord, TrainingPlanExerciseInfo,\
    TrainingExercise
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'The user with the given login already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()

        password = mutable_data.get('password')
        hashed_password = make_password(password)
        mutable_data['password'] = hashed_password
        print(mutable_data)

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


class CreateUserTrainingPlan(generics.CreateAPIView):
    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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


class ReadUserTrainingPlans(generics.ListAPIView):
    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserTrainingPlans.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserTrainingPlan(generics.UpdateAPIView):
    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> UserTrainingPlans:
        user = self.request.user.id
        plan_id = self.kwargs.get('pk')

        try:
            training_plan = UserTrainingPlans.objects.get(pk=plan_id, user=user)
            return training_plan

        except UserTrainingPlans.DoesNotExist:
            self.permission_denied(self.request)


class DeleteUserTrainingPlan(generics.DestroyAPIView):
    queryset = UserTrainingPlans.objects.all()
    serializer_class = UserTrainingPlansSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> UserTrainingPlans:
        user = self.request.user.id
        plan_id = self.kwargs.get('pk')

        try:
            training_plan = UserTrainingPlans.objects.get(pk=plan_id, user=user)
            return training_plan
        except UserTrainingPlans.DoesNotExist:
            print('lol')
            self.permission_denied(self.request)


class CreateTraining(generics.CreateAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
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

class ReadTrainings(generics.ListAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Training.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTraining(generics.UpdateAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> Training:
        user = self.request.user.id
        training_id = self.kwargs.get('pk')

        try:
            training = Training.objects.get(pk=training_id, user=user)
            return training
        except Training.DoesNotExist:
            self.permission_denied(self.request)


class DestroyTraining(generics.DestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> Training:
        user = self.request.user.id
        training_id = self.kwargs.get('pk')

        try:
            training = Training.objects.get(pk=training_id, user=user)
            return training
        except Training.DoesNotExist:
            self.permission_denied(self.request)


class CreateTrainingRecord(generics.CreateAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReadTrainingRecord(generics.ListAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.kwargs.get('user')
        request_user = self.request.user.id

        if request_user != user:
            self.permission_denied(self.request)

        return TrainingRecord.objects.get(user=user)


class UpdateTrainingRecord(generics.UpdateAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.request.user.id
        record_id = self.kwargs.get('pk')

        try:
            record = TrainingRecord.objects.get(pk=record_id, user=user)
            return record

        except TrainingRecord.DoesNotExist:
            self.permission_denied(self.request)


class DestroyTrainingRecord(generics.DestroyAPIView):
    queryset = TrainingRecord.objects.all()
    serializer_class = TrainingRecordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingRecord:
        user = self.request.user.id
        record_id = self.kwargs.get('pk')
        try:
            training = TrainingRecord.objects.get(pk=record_id, user=user)
            return training
        except TrainingRecord.DoesNotExist:
            self.permission_denied(self.request)

class CreateTrainingPlanExerciseInfo(generics.CreateAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReadTrainingPlanExerciseInfo(generics.ListAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self) -> TrainingPlanExerciseInfo:
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class UpdateTrainingPlanExerciseInfo(generics.UpdateAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class DestroyTrainingPlanExerciseInfo(generics.DestroyAPIView):
    queryset = TrainingPlanExerciseInfo.objects.all()
    serializer_class = TrainingPlanExerciseInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info
#TODO od tego momentu brak testów do api


class CreateTrainingExercise(generics.CreateAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReadTrainingExercise(generics.ListAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        exercise_info_id = self.kwargs.get('pk')
        exercise_info = TrainingPlanExerciseInfo.objects.get(pk=exercise_info_id)

        return exercise_info


class UpdateTrainingExercise(generics.UpdateAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class DestroyTrainingExercise(generics.DestroyAPIView):
    queryset = TrainingExercise.objects.all()
    serializer_class = TrainingExerciseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]