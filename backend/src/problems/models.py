from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db.models import Max
from django.dispatch import receiver

from problems.storage import OverwriteStorage
from accounts.models import Profile
from tags.models import Tag

from django.core.urlresolvers import reverse



# Create your models here.

class Problem(models.Model):
	""" Represents a programming problem on the website"""

	title = models.CharField(max_length=255)
	problem_code = models.CharField(max_length=100, unique = True)
	slug = models.SlugField(unique = True) # Slug Field
	statement = models.TextField() #Problem statement
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	setter = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='setter')
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.problem_code

	def get_absolute_url(self):
		return reverse("problem", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-timestamp"]



def upload_input(instance, filename):
	return "%s/%s.in" %(instance.problem_id.problem_code, instance.testcase)

def upload_output(instance, filename):
	return "%s/%s.out" %(instance.problem_id.problem_code, instance.testcase)

class TestCase(models.Model):

	problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE) # A problem has many test cases
	input = models.FileField(upload_to = upload_input, storage=OverwriteStorage())
	output = models.FileField(upload_to = upload_output, storage=OverwriteStorage())
	sample = models.BooleanField()
	weight = models.IntegerField(null = False, blank = False, default = 0)
	testcase = models.IntegerField();

	def __str__(self):
		return "%s-%s"%(self.problem_id.problem_code, self.testcase);

	class Meta:
		unique_together = ('problem_id', 'testcase')

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	slug = slugify(instance.problem_code)
	exists = Problem.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

@receiver(pre_save, sender=TestCase)
def pre_save_testcase_number(sender, instance, *args, **kwagrs):
	exists = TestCase.objects.filter(problem_id = instance.problem_id).exists()
	instance.testcase = 1
	if exists:
		instance.testcase = 1 + TestCase.objects.filter(problem_id = instance.problem_id).aggregate(Max('testcase'))["testcase__max"]

pre_save.connect(pre_save_post_receiver, sender = Problem)
