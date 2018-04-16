from django.contrib import admin

from .models import Profile
# Register your models here.

class ProfileAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["user"]

	search_fields = ["user", "user.email"]

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdminModel)
