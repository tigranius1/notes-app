from django.shortcuts import render
from .models import Note


def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/list.html', {'notes': notes})