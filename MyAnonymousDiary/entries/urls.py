from django.conf.urls import url, re_path
from .views import EntryDetailView, EntryUpdateView

urlpatterns = [
  url(r'^entry/(?P<pk>[^/]+)/$', EntryDetailView.as_view(), name='entry_detail'),
  url(r'^entry/(?P<pk>[^/]+)/edit/', EntryUpdateView.as_view(), name='edit_entry'),
]