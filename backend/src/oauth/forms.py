from allauth.account.forms import LoginForm

class AuthLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(AuthLoginForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
