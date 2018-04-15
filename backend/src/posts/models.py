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
	slug = slugify(instance.title)
	exists = Post.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Post)
