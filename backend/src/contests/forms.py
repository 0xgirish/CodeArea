from django import forms
from pagedown.widgets import PagedownWidget

from .models import Contest

class ContestForm(forms.ModelForm):

	start_contest = forms.DateTimeField(widget=forms.DateTimeInput(),input_formats=['%m/%d/%Y %I:%M %p'])
	end_contest = forms.DateTimeField(widget=forms.DateTimeInput(),input_formats=['%m/%d/%Y %I:%M %p'])
	description = forms.CharField(widget=PagedownWidget(show_preview=False))

	class Meta:
		model = Contest
		fields = [
			"title", 
			"contest_code",
			"description",
			"start_contest",
			"end_contest",
			"private",
		]

	def __init__(self, *args, **kwargs):
		super(ContestForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['contest_code'].required = False
			self.fields['contest_code'].widget.attrs['disabled'] = True

		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

		self.fields['start_contest'].widget.attrs.update({'class': 'form-group form-control datetimepicker'})
		self.fields['end_contest'].widget.attrs.update({'class': 'form-group form-control datetimepicker'})

	def clean_contest_code(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.contest_code
		else:
			return self.cleaned_data['contest_code']
