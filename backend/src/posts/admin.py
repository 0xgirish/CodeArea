from django.contrib import admin

# Register your models here.

from .models import Post, Comment, CommentReply

class PostModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["title", "content", "author"]

	# Search Fields
	search_fields = ["title", "tags"]

	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)

class CommentModelAdmin(admin.ModelAdmin):
	""" Problem Admin Model """

	# Display  Fields
	list_display = ["user", "content", "post"]

	# Search Fields
	search_fields = ["post", "user"]

	class Meta:
		model = Comment

admin.site.register(Comment, CommentModelAdmin)

class CommentReplyAdmin(admin.ModelAdmin):
	# Display  Fields
	list_display = ["user", "content", "parent"]

	# Search Fields
	search_fields = ["parent", "user"]

	class Meta:
		model = CommentReply

admin.site.register(CommentReply, CommentReplyAdmin)
