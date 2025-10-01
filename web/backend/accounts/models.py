from django.db import models


class LoginAttempt(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=128)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.email} at {self.timestamp}"
