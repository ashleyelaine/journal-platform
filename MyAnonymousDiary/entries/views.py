from django.shortcuts import render
from django.utils import timezone
from .models import Entry

# Create your views here.
def entry_list(request):
    entries = Entry.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'pages/home.html', {'entries': entries})