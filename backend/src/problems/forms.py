from django import forms

from pagedown.widgets import PagedownWidget

from .models import Problem, TestCase
from tags.models import Tag

class ProblemForm(forms.ModelForm):
	statement = forms.CharField(widget=PagedownWidget(show_preview=False))
	datetime = forms.DateField(widget=forms.DateTimeInput(),input_formats=['%Y-%m-%d %I:%M %p'])
	class Meta:
		model = Problem
		fields = [
			"title", 
			"problem_code",
			"statement",
			"tags",
			"datetime",
		]

	def __init__(self, *args, **kwargs):
		super(ProblemForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['problem_code'].required = False
			self.fields['problem_code'].widget.attrs['disabled'] = True


		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

		self.fields['datetime'].widget.attrs.update({'class': 'form-group form-control datetimepicker'})


	def clean_problem_code(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.problem_code
		else:
			return self.cleaned_data['problem_code']

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
