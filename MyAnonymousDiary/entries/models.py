from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class Entry(models.Model):
  class Meta:
    verbose_name_plural = "entries"

  author = models.ForeignKey('users.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  content = models.TextField()
  slug = models.SlugField(default='', blank=True, null=True)
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True) 

  def publish(self):
    self.published_date = timezone.now()
    self.slug = slugify(self.title)
    self.save()

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)
        