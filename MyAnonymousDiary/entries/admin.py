from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry
from django.contrib.auth.models import User

# Register your models here.

class EntryAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('content',)

    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Entry, EntryAdmin)