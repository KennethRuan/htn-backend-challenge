from rest_framework import serializers
from .models import Hacker, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'rating')

class HackerSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(source="skill_set", many=True)

    class Meta:
        model = Hacker
        fields = ('name', 'company', 'email', 'phone', 'skills')

class SkillAggregationSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
