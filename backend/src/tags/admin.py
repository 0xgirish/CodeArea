from django.contrib import admin

# Register your models here.

from .models import Tag

class TagModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["name", "description"]

	# Search Fields
	search_fields = ["name"]

	class Meta:
		model = Tag

admin.site.register(Tag, TagModelAdmin)
