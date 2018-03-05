from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.

class Problem(models.Model):
	""" Represents a programming problem on the website"""

	title = models.CharField(max_length=255)
	problem_code = models.CharField(max_length=100, unique = True)
	slug = models.SlugField(unique = True) # Slug Field
	statement = models.TextField() #Problem statement
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __str__(self):
		return self.problem_code

	class Meta:
		ordering = ["-timestamp"]


class TestCase(models.Model):

	problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE) # A problem has many test cases
	input = models.FileField(upload_to = "%s/%s.in"%("testcase", id))
	output = models.FileField(upload_to = "%s/%s.out"%("testcase", id))
	sample = models.BooleanField() 

	def __str__(self):
		return "%s-%s"%(self.problem_id.problem_code, self.id);

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	slug = slugify(instance.problem_code)
	exists = Problem.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Problem)
