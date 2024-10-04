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


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = '__all__'


class ExercisesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['body_part'] = BodyPartSerializer(
               instance.body_part.all(), many=True, context=self.context
            ).data

        return representation



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
