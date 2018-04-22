from django.conf import settings
from rest_framework import serializers
from . import models

class SubmissionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Submission
		fields = '__all__'
