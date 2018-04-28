from django.db import models
from accounts.models import Profile
from tags.models import Tag

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(unique = True) # Slug Field
	content = models.TextField() 
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	author = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='author')
	likes = models.ManyToManyField(Profile, blank=True, related_name='post_likes')
	tags = models.ManyToManyField(Tag, blank=True)

	def get_absolute_url(self):
		return reverse("post", kwargs={"slug": self.slug})

	def get_likes_url(self):
		return reverse("post_likes", kwargs={"slug": self.slug})

	def get_likes_api_url(self):
		return reverse("post_likes_api", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	exists = Post.objects.filter(title = instance.title).exists()
	if not exists:
		slug = slugify(instance.title)
		instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Post)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	user = models.ForeignKey(Profile, on_delete = models.CASCADE)
	content = models.TextField()

	def __str__(self):
		return "%s-%s-%s"%(self.user.user.username, self.post.title, self.id)

class CommentReply(models.Model):
	parent = models.ForeignKey(Comment, on_delete = models.CASCADE)
	user = models.ForeignKey(Profile, on_delete = models.CASCADE)
	content = models.TextField()

	def __str__(self):
		return "%s-%s-%s"%(self.user.username, self.parent.id, self.id)
