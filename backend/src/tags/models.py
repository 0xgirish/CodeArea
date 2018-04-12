from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=255)
	slug = models.SlugField(unique = True) # Slug Field

	def __str__(self):
		return self.name

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	slug = slugify(instance.name)
	exists = Tag.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Tag)
