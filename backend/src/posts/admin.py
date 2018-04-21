from django.contrib import admin

# Register your models here.

from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["title", "content", "author"]

	# Search Fields
	search_fields = ["title", "tags"]

	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
