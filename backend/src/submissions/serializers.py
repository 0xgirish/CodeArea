from django.conf import settings
from rest_framework import serializers
from . import models

class SubmissionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Submission
		fields = '__all__'

class SubmissionTasksSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.SubmissionTasks
		fields = '__all__'

class ContestSubmissionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ContestSubmission
		fields = '__all__'