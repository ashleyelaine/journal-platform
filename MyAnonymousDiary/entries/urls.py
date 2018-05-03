from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, re_path, include
from .views import EntryDetailView, EntryUpdateView, EntryCreateView

urlpatterns = [
  url(r'^entry/create/$', EntryCreateView.as_view(), name='edit_entry'),
  url(r'^entry/(?P<pk>[^/]+)/$', EntryDetailView.as_view(), name='entry_detail'),
  url(r'^entry/(?P<pk>[^/]+)/edit/$', EntryUpdateView.as_view(), name='edit_entry'),
  url(r'^summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)