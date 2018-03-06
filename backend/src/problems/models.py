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



def upload_input(instance, filename):
	return "%s/%s.in" %(instance.problem_id.problem_code, instance.testcase_number())

def upload_output(instance, filename):
	return "%s/%s.out" %(instance.problem_id.problem_code, instance.testcase_number())

class TestCase(models.Model):

	problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE) # A problem has many test cases
	input = models.FileField(upload_to = upload_input)
	output = models.FileField(upload_to = upload_output)
	sample = models.BooleanField()
	weight = models.IntegerField(null = False, blank = False, default = 0)

	def __str__(self):
		return "%s-%s"%(self.problem_id.problem_code, self.testcase_number());

	def testcase_number(self):
		count = TestCase.objects.filter(problem_id = self.problem_id).count()
		return count

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	slug = slugify(instance.problem_code)
	exists = Problem.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Problem)
