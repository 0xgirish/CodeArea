from django.db import models

# Create your models here.

class Problem(models.Model):
	""" Represents a programming problem on the website"""

	title = models.CharField(max_length=255)
	slug = models.SlugField(unique = True) # Slug Field
	statement = models.TextField() #Problem statement

class TestCase(models.Model):

	problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE) # A problem has many test cases
	input = models.FileField(upload_to = "%s/%s.in"%("testcase", id))
	output = models.FileField(upload_to = "%s/%s.out"%("testcase", id))
	sample = models.BooleanField() 
