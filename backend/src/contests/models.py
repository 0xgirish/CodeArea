from django.db import models

from problems.models import Problem
from accounts.models import Profile

from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here
from django.core.urlresolvers import reverse



class Contest(models.Model):
	""" Model Representing a contest """

	title = models.CharField(max_length = 255)
	description = models.TextField()
	contest_code = models.CharField(max_length = 100, unique = True)
	slug = models.SlugField(unique = True)
	creator = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='creator')
	
	problems = models.ManyToManyField(Problem, through = 'ContestsHaveProblems')
	creation_date = models.DateField(auto_now = False, auto_now_add = True)
	start_contest = models.DateTimeField(auto_now = False, auto_now_add = False)
	end_contest = models.DateTimeField(auto_now = False, auto_now_add = False)
	participants = models.ManyToManyField(Profile, through = 'Participant')

	def __str__(self):
		return self.contest_code;

	def get_absolute_url(self):
		return reverse("contest_problem_list", kwargs={"slug": self.slug})


	class Meta:
		ordering = ["-creation_date"]



class ContestsHaveProblems(models.Model):
	""" The many to many relation """

	problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
	contest = models.ForeignKey(Contest, on_delete = models.CASCADE)
	weight = models.IntegerField(null = False, blank = False, default = 0)

	def __str__(self):
		return "%s-%s" %(self.contest.contest_code, self.problem.problem_code)

	def get_absolute_url(self):
		return reverse("contest_problem", kwargs={"slug1": self.contest.slug, "slug2": self.problem.slug})


	class Meta:
		verbose_name = 'Contest Problem'
		unique_together = ('problem', 'contest')


class Participant(models.Model):
	""" A participant of a contest """
	user = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'participant')
	contest = models.ForeignKey(Contest, on_delete = models.CASCADE)
	points = models.IntegerField(null = False, blank = False, default = 0)

	def __str__(self):
		return "%s: %s" %(self.contest.contest_code, self.user.user.username)

	class Meta:
		unique_together = ('user', 'contest')

def pre_save_post_receiver(sender, instance, *args, **kwagrs):
	slug = slugify(instance.contest_code)
	exists = Contest.objects.filter(slug = slug).exists()
	if exists:
		# Won't exist because problem_code is unique but just in case
		slug = "%s-%s"%(slug, instance.id)

	instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Contest)

