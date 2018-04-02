from django import forms

from pagedown.widgets import PagedownWidget

from .models import Problem, TestCase

class ProblemForm(forms.ModelForm):
	statement = forms.CharField(widget=PagedownWidget(show_preview=False))
	class Meta:
		model = Problem
		fields = [
			"title", 
			"problem_code",
			"statement",
		]

	def __init__(self, *args, **kwargs):
		super(ProblemForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
