from rest_framework import serializers
from trainings.models import BodyPart, Exercise, UserTrainingPlans, Training, TrainingRecord, TrainingExercise,\
    TrainingPlanExerciseInfo
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class Calculate1RMSerializer(serializers.Serializer):
    reps = serializers.IntegerField()
    lift = serializers.FloatField()


class PointsCalculatorSerializer(serializers.Serializer):
    female = serializers.BooleanField()
    body = serializers.FloatField()
    lift = serializers.FloatField()


class CalculateTotalSerializer(serializers.Serializer):
    female = serializers.BooleanField()
    body = serializers.FloatField()
    sq = serializers.FloatField()
    sq_reps = serializers.IntegerField()
    bp = serializers.FloatField()
    bp_reps = serializers.IntegerField()
    dl = serializers.FloatField()
    dl_reps = serializers.IntegerField()


class CalculatorResultSerializer(serializers.Serializer):
    result = serializers.FloatField()


class TotalCalculatorResultSerializer(serializers.Serializer):
    gender = serializers.CharField()
    weight = serializers.FloatField()
    squat = serializers.FloatField()
    squat_wilks = serializers.FloatField()
    squat_dots = serializers.FloatField()
    squat_ipf_gl = serializers.FloatField()
    bench_wilks = serializers.FloatField()
    bench_dots = serializers.FloatField()
    bench_ipf_gl = serializers.FloatField()
    deadlift_wilks = serializers.FloatField()
    deadlift_dots = serializers.FloatField()
    deadlift_ipf_gl = serializers.FloatField()
    total = serializers.FloatField()
    total_wilks = serializers.FloatField()
    total_dots = serializers.FloatField()
    total_ipf_gl = serializers.FloatField()


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = '__all__'




class ExercisesSerializer(serializers.ModelSerializer):
    # body_part = BodyPartSerializer(many=True)
    # body_part = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['body_part'] = BodyPartSerializer(
               instance.body_part.all(), many=True, context=self.context
            ).data

        return representation

    # @staticmethod
    # def get_body_part(obj):
    #     return [body_part.name for body_part in obj.body_part.all()]


class UserTrainingPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrainingPlans
        fields = "__all__"



class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"


class TrainingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingRecord
        fields = "__all__"


class TrainingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingExercise
        fields = "__all__"


class TrainingPlanExerciseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlanExerciseInfo
        fields = "__all__"
