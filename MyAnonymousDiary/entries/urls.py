from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, re_path, include
from .views import EntryDetailView, EntryUpdateView, EntryCreateView, EntryDeleteView

urlpatterns = [
  url(r'^entry/new/$', EntryCreateView.as_view(), name='new_entry'),
  url(r'^entry/(?P<pk>[^/]+)/$', EntryDetailView.as_view(), name='entry_detail'),
  url(r'^entry/(?P<pk>[^/]+)/edit/$', EntryUpdateView.as_view(), name='edit_entry'),
  url(r'^entry/(?P<pk>[^/]+)/delete/$', EntryDeleteView.as_view(), name='delete_entry'),
  url(r'^summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)