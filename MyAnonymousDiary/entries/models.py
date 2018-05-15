from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class EntryQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def is_draft(self):
        return self.filter(draft=True)

    def is_not_draft(self):
        return self.filter(draft=False)

    def is_active(self):
        return self.filter(draft=True)
    
    def is_update(self):
        return self.filter(update=True)

    def is_not_update(self):
        return self.filter(update=False)


class EntryManager(models.Manager):
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)

    def is_public(self):
        return self.get_queryset().is_public()

    def is_draft(self):
        return self.get_queryset().is_draft()

    def is_not_draft(self):
        return self.get_queryset().is_not_draft()

    def is_active(self):
        return self.get_queryset().is_active()

    def is_update(self):
        return self.get_queryset().is_update()

    def is_not_update(self):
        return self.get_queryset().is_not_update()


class Entry(models.Model):
    class Meta:
        verbose_name_plural = "entries"
    
    objects = EntryManager()

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(default='', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    draft = models.BooleanField(default=False, verbose_name='Is draft')
    public = models.BooleanField(default=False, verbose_name='Is public')
    active = models.BooleanField(default=True, verbose_name='Is Active')
    update = models.BooleanField(default=False, verbose_name='Is Update')

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.slug = slugify(self.title)
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        