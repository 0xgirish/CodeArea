from django import forms

from pagedown.widgets import PagedownWidget

from .models import Problem, TestCase

class ProblemForm(forms.ModelForm):
	statement = forms.CharField(widget=PagedownWidget)
	class Meta:
		model = Problem
		fields = [
			"title", 
			"problem_code",
			"statement",
		]