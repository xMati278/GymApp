from rest_framework import serializers


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