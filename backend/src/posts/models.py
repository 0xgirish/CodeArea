from django.db import models
from accounts.models import Profile
from tags.models import Tag

from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(unique = True) # Slug Field
	content = models.TextField() 
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	author = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='author')
	tags = models.ManyToManyField(Tag)

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
