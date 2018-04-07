from django import forms

from pagedown.widgets import PagedownWidget

from .models import Problem, TestCase
from tags.models import Tag

class ProblemForm(forms.ModelForm):
	statement = forms.CharField(widget=PagedownWidget(show_preview=False))
	datetime = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
	class Meta:
		model = Problem
		fields = [
			"title", 
			"problem_code",
			"statement",
			"tags",
			"datetime"
		]

	def __init__(self, *args, **kwargs):
		super(ProblemForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class TestCaseForm(forms.ModelForm):
	class Meta:
		model = TestCase
		fields = [
			"input", 
			"output",
			"sample",
			"weight",
			"explanation",
		]

	def __init__(self, *args, **kwargs):
		super(TestCaseForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
