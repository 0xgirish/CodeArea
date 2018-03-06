from django.contrib import admin

# Register your models here.

from .models import Submission, ContestSubmission

class SubmissionModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["user", "problem", "timestamp", "status"]

	# Search Fields
	search_fields = ["problem", "user"]

	class Meta:
		model = Submission

admin.site.register(Submission, SubmissionModelAdmin)


class ContestSubmissionModelAdmin(admin.ModelAdmin):
	""" TestCase Admin Model """

	# Display  Fields
	list_display = ["user", "problem", "timestamp", "status"]

	# Search Fields
	search_fields = ["problem", "user"]

	class Meta:
		model = ContestSubmission

admin.site.register(ContestSubmission, ContestSubmissionModelAdmin)
