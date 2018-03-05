from django.contrib import admin

# Register your models here.
from .models import Problem, TestCase

class ProblemModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["problem_code", "title"]

	# Search Fields
	search_fields = ["problem_code", "title", "statement"]

	class Meta:
		model = Problem

admin.site.register(Problem, ProblemModelAdmin)


class TestCaseModelAdmin(admin.ModelAdmin):
	""" TestCase Admin Model """
	class Meta:
		model = TestCase

admin.site.register(TestCase, TestCaseModelAdmin)