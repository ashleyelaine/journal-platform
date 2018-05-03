from django import forms
from django_summernote.widgets import SummernoteWidget

from entries.models import Entry


class EntryForm(forms.ModelForm):
  class Meta:
      model = Entry
      fields = ('title', 'content')
      widgets = {
        'content': SummernoteWidget(),
      }