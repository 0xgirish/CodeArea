from django.conf import settings
from rest_framework import serializers
from . import models

class TestCaseSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.TestCase
		exclude = ('testcase',)
