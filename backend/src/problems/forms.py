from django import forms

from .models import Problem, TestCase

class ProblemForm(forms.ModelForm):
	class Meta:
		model = Problem
		fields = [
			"title", 
			"problem_code"
		]