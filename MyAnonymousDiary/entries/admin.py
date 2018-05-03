from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry

# Register your models here.

class EntryAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Entry, EntryAdmin)