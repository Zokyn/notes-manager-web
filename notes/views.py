from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from .models import Note, Body

# Create your views here.
def index(request):
    latest_note_list = Note.objects.order_by("-pub_date")[:10]
    context = {
        "latest_note_list": latest_note_list
    }
    return render(request, "notes/index.html", context)

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

def edit(request, note_id, body_id):
    note = get_object_or_404(Note, pk=note_id)
    try: 
        body = get_object_or_404(Body, pk=body_id)
        context = {
            "note": note,
            "body": body
        }
        return render(request, 'notes/edit.html', context)
    except (KeyError, Body.DoesNotExist):
        error = "Can't reach selected body. This note doesn't have this body linked"
        messages.error(request, error)
    return redirect('notes:index')

def post(request : HttpRequest, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == "POST":
        body = get_object_or_404(Body, pk=request.POST["body_id"])
        try: 
            body.body_text = request.POST.get("text", '')
            body.save()
        except (KeyError, Note.DoesNotExist):
            context = {
                "note": note,
                "error_message": "Essa nota não existe"
            }
            return render(request, "notes:note", context)
    else:
        error = "Request doens't have method post"
        messages.error(request, error)
    return redirect("notes:index")
