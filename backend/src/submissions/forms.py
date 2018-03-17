from django import forms

from .models import Submission, ContestSubmission

class SubmissionForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = [
			"code", 
			"language",
		]

class ContestSubmissionForm(forms.ModelForm):
	class Meta:
		model = ContestSubmission
		fields = [
			"code", 
			"language",
		]