from django.contrib import admin

# Register your models here.

from .models import Contest, ContestsHaveProblems

class ContestModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["contest_code", "title", "start_contest", "end_contest"]

	# Search Fields
	search_fields = ["contest_code", "title", "description"]

	class Meta:
		model = Contest

admin.site.register(Contest, ContestModelAdmin)


class ContestsHaveProblemsModelAdmin(admin.ModelAdmin):
	""" TestCase Admin Model """
	class Meta:
		model = ContestsHaveProblems

admin.site.register(ContestsHaveProblems, ContestsHaveProblemsModelAdmin)
