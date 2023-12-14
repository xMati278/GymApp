from rest_framework import serializers
from trainings.models import BodyPart, Exercise


class Calculate1RMSerializer(serializers.Serializer):
    reps = serializers.IntegerField()
    weight = serializers.FloatField()


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


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = '__all__'


class GetExercisesSerializer(serializers.ModelSerializer):
    body_part = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'user']

    @staticmethod
    def get_body_part(obj):
        return [body_part.name for body_part in obj.body_part.all()]

