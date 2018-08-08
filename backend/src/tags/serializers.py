from django.conf import settings
from rest_framework import serializers
from . import models

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Tag
		exclude = ('slug',)