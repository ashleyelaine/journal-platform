from django.contrib.sites.models import Site
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _, ugettext_lazy as _l
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView
from .models import Entry

# ENTRY LIST VIEW
class EntryListView(ListView):
  def get_queryset(self):
    queryset = Entry.objects.all()
    return queryset


# ENTRY DETAIL VIEW
class EntryDetailView(DetailView):
    queryset = Entry.objects.all()

    def get_entry(self, *args, **kwargs):
        entry_id = self.kwargs.get('pk')
        entry = get_object_or_404(Entry, id=entry_id)
        return entry


# ENTRY UPDATE VIEW
class EntryUpdateView(UpdateView):
    model = Entry
    fields = ('title', 'text')
    template_name = 'entries/entry_edit.html'
    success_url = reverse_lazy('entry_detail')
    success_message = _('The entry has been updated')