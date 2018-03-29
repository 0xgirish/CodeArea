from django import forms


from .models import Contest

class ContestForm(forms.ModelForm):

	start_contest = forms.DateTimeField(widget = forms.widgets.SplitDateTimeWidget())
	end_contest = forms.DateTimeField(widget = forms.widgets.SplitDateTimeWidget())

	class Meta:
		model = Contest
		fields = [
			"title", 
			"contest_code",
			"description",
			"start_contest",
			"end_contest",
		]