from django.conf import settings
from rest_framework import serializers
from . import models

class ContestsHaveProblemsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ContestsHaveProblems
		fields = '__all__'

class ContestSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Contest
		exclude = ('creation_date', 'problems', )
		

