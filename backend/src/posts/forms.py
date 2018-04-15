from django import forms

from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	class Meta:
		model = Post
		fields = [
			"title", 
			"content",
			"tags",
		]

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'