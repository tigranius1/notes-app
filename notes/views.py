from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Note
from .forms import NoteForm


def note_list(request):
    query = request.GET.get('q', '').strip()
    notes = Note.objects.all().order_by('-created_at')
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(text__icontains=query))
    return render(request, 'notes/list.html', {'notes': notes, 'query': query})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/create.html', {'form': form})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/detail.html', {'note': note})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/update.html', {'form': form, 'note': note})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/delete.html', {'note': note})