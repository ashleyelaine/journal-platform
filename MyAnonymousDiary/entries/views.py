from django.contrib.sites.models import Site
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _, ugettext_lazy as _l
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import EntryForm, EntryFormSuper
from .models import Entry

# ENTRY LIST VIEW / HOME?
class EntryListView(ListView):
    template_name= 'pages/home.html'
    context_object_name = 'entry_list'

    def get_queryset(self):
        queryset = Entry.objects.is_public().is_not_update().is_not_draft()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        updates = Entry.objects.is_public().is_update().is_not_draft().order_by('created_date').reverse()[:2]
        context['updates_list'] = updates
        return context


# UPDATES LIST VIEW
class UpdatesListView(ListView):
    template_name='pages/updates.html'

    def get_queryset(self):
        queryset = Entry.objects.is_public().is_update()
        return queryset


# ENTRY DETAIL VIEW
class EntryDetailView(DetailView):
    queryset = Entry.objects.all()

    def get_entry(self, *args, **kwargs):
        entry_id = self.kwargs.get('pk')
        entry = get_object_or_404(Entry, id=entry_id)
        return entry


# ENTRY UPDATE VIEW
class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_edit.html'
    success_message = _('The entry has been updated')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('entry_detail', args=[self.get_object().pk])

    def form_valid(self, form):
        if 'save_as_draft' in self.request.POST:
            form.instance.draft = True

        elif 'publish' in self.request.POST:
            form.instance.draft = False
            form.instance.published_date = timezone.now()

        form.instance.author = self.request.user
        return super().form_valid(form)


# ENTRY CREATE VIEW
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_create.html'
    success_message = _('The entry has been added')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return EntryFormSuper
        else:
            return EntryForm
        
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('new_entry')

    def form_valid(self, form):
        if 'save_as_draft' in self.request.POST:
            form.instance.draft = True

        elif 'publish' in self.request.POST:
            form.instance.draft = False
            form.instance.published_date = timezone.now()

        form.instance.author = self.request.user
        return super().form_valid(form)


# ENTRY DELETE VIEW
class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'entries/entry_delete.html'
    success_message = _('The entry has been deleted')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('users:detail', kwargs={'username': self.request.user.username})
