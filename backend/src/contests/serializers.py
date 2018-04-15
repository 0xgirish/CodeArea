from django.conf import settings
from rest_framework import serializers
from . import models

class ContestsHaveProblemsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ContestsHaveProblems
		fields = '__all__'
		

