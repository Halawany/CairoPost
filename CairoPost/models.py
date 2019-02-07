from django.db import models
from django.conf import settings
from django.utils import timezone

# Creating my blog model 
class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.pub_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title