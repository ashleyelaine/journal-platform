from django.contrib.sites.models import Site
from django.views.generic import ListView
from django.utils import timezone
from .models import Entry

# ENTRY LIST VIEW
class EntryListView(ListView):
  def get_queryset(self):
    queryset = Entry.objects.all()
    return queryset