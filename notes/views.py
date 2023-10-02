from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from .forms import BodyForm
from .models import Note, Body

# Create your views here.

class NoteListView(ListView):
    model = Note
    context_object_name = "latest_note_list"
    template_name = "notes/index.html"

def note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    try: 
        body_list = note.body_set.all()
        context = {
            "note": note,
            "body_list": body_list
        }
    except (KeyError, Body.DoesNotExist):
        context = {
            "note": note,
            "error_message": "There is no bodies on this note"
        }
        return render(request, "notes/note.html", context)
    return render(request, "notes/note.html", context)

def new(request, note_id):
    note = Note.objects.get(pk=note_id)
    
    if request.method == 'POST':
        form = BodyForm(request.POST)
        if form.is_valid():
            body = form.save(commit=False)
            body.note = note
            body.save()
        return redirect('notes:index')
    else:
        form = BodyForm()
    return render(request, "notes/new.html", {'note': note, 'form': form})
    
def edit(request, note_id, body_id):
    note = Note.objects.get(pk=note_id)
    body = Body.objects.get(pk=body_id)
    
    if request.method == 'POST':
        form = BodyForm(request.POST, instance=body)
        if form.is_valid():
            body.save()
            return redirect('notes:index')
    else:
        form = BodyForm(instance=body)
    return render(request, "notes/edit.html", {'note': note, 'body': body, 'form': form})