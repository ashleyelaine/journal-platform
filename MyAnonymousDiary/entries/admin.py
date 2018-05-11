from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry
from django.contrib.auth.models import User

# Register your models here.

class EntryAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'active', 'public', 'draft')
    search_fields =  ['title','author__username']

admin.site.register(Entry, EntryAdmin)