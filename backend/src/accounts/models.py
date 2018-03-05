from django.db import models

# Create your models here.

class Profile(models.Model):
	""" A Model Representing a User Profile"""
	
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
