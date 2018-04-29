from allauth.account.forms import LoginForm,SignupForm,ResetPasswordForm
from django import forms

class AuthLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(AuthLoginForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

		self.fields['remember'].widget.attrs['class'] = ''

class AuthSignupForm(SignupForm):
	def __init__(self, *args, **kwargs):
		super(AuthSignupForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
						
class AuthResetPasswordForm(ResetPasswordForm):
	def __init__(self, *args, **kwargs):
		super(AuthResetPasswordForm, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	
