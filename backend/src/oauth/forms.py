from allauth.account.forms import LoginForm,SignupForm

class AuthLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(AuthLoginForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class AuthSignupForm(SignupForm):
	def __init__(self, *args, **kwargs):
		super(AuthSignupForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
						
