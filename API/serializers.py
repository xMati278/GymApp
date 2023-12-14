from rest_framework import serializers
from trainings.models import BodyPart


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = '__all__'


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