from django import forms


from .models import Contest

class ContestForm(forms.ModelForm):

	start_contest = forms.DateField(widget=forms.DateTimeInput())
	end_contest = forms.DateField(widget=forms.DateTimeInput())

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
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

		self.fields['start_contest'].widget.attrs.update({'class': 'form-group form-control datetimepicker', 'value':'10/05/2016'})
		self.fields['end_contest'].widget.attrs.update({'class': 'form-group form-control datetimepicker', 'value':'10/05/2016'})