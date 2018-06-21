from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db.models import Max
from django.dispatch import receiver
from django.conf import settings

from problems.storage import OverwriteStorage
from accounts.models import Profile
from tags.models import Tag

from django.core.urlresolvers import reverse



def upload_solution(instance, filename):
	extension = filename.split(".")[-1]
	return "%s/solution.%s" %(instance.problem_code, extension)

class Problem(models.Model):
	""" Represents a programming problem on the website"""

	LEVEL_CHOICES = (
		('EASY', 'Easy'),
		('MEDIUM', 'Medium'),
		('HARD', 'Hard')
	)

	title = models.CharField(max_length=255)
	problem_code = models.CharField(max_length=100, unique = True)
	slug = models.SlugField(unique = True) # Slug Field
	statement = models.TextField() #Problem statement
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	setter = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='setter')
	tags = models.ManyToManyField(Tag, blank=True)
	level = models.CharField(max_length=10, choices= LEVEL_CHOICES, default = 'EASY')
	unlisted = models.BooleanField(default=False)

	solution_checker = models.FileField(upload_to = upload_solution,storage=OverwriteStorage(), blank = True, null = True)
	time_limit = models.IntegerField(default = 2)
	memory_limit = models.FloatField(blank = True, null = True)

	def __str__(self):
		return self.problem_code

	def get_absolute_url(self):
		return reverse("problem", kwargs={"slug": self.slug})

	def get_sample(self):
		queryset = TestCase.objects.filter(problem = self, sample = True)
		print(queryset)
		return queryset

	class Meta:
		ordering = ["-timestamp"]



def upload_input(instance, filename):
	return "%s/%s.in" %(instance.problem.problem_code, instance.testcase)

def upload_output(instance, filename):
	return "%s/%s.out" %(instance.problem.problem_code, instance.testcase)

class TestCase(models.Model):

	problem = models.ForeignKey(Problem, on_delete=models.CASCADE) # A problem has many test cases
	input = models.FileField(upload_to = upload_input, storage=OverwriteStorage())
	output = models.FileField(upload_to = upload_output, storage=OverwriteStorage())
	sample = models.BooleanField()
	explanation = models.CharField(max_length=255, blank=True, null=True)
	weight = models.IntegerField(null = False, blank = False, default = 0)
	testcase = models.IntegerField();

	def __str__(self):
		return "%s-%s"%(self.problem.problem_code, self.testcase);

	def get_api_url(self):
		return reverse("testcase-detail", kwargs={"pk": self.pk})

	def input2string(self):
		self.input.open("rb")
		return(self.input.read())

	def output2string(self):
		self.output.open("rb")
		# print(self.output.read())
		return(self.output.read())


	class Meta:
		unique_together = ('problem', 'testcase')

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	exists = Problem.objects.filter(problem_code = instance.problem_code).exists()
	if not exists:
		slug = slugify(instance.problem_code)
		instance.slug = slug

@receiver(pre_save, sender=TestCase)
def pre_save_testcase_number(sender, instance, *args, **kwagrs):
	exists = TestCase.objects.filter(problem = instance.problem).exists()
	instance.testcase = 1
	if exists:
		instance.testcase = 1 + TestCase.objects.filter(problem = instance.problem).aggregate(Max('testcase'))["testcase__max"]

pre_save.connect(pre_save_post_receiver, sender = Problem)
