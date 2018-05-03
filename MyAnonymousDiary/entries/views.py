from django.contrib.sites.models import Site
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _, ugettext_lazy as _l
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from .forms import EntryForm
from .models import Entry

# ENTRY LIST VIEW / HOME?
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
    form_class = EntryForm
    template_name = 'entries/entry_edit.html'
    success_message = _('The entry has been updated')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('entry_detail', args=[self.get_object().pk])

# ENTRY CREATE VIEW
class EntryCreateView(TemplateView):
    template_name = 'entries/entry_create.html'
    

    
    