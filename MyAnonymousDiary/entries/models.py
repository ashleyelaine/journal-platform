from django.db import models
from django.utils import timezone


class Entry(models.Model):
  class Meta:
    verbose_name_plural = "entries"

  author = models.ForeignKey('users.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(
          default=timezone.now)
  published_date = models.DateTimeField(
          blank=True, null=True)

  def publish(self):
      self.published_date = timezone.now()
      self.save()

  def __str__(self):
      return self.title