from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
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

def edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    try: 
        body = note.body_set.get(pk=request.POST["body_id"])
        context = {
            "note": note,
            "body": body
        }
    except (KeyError, Body.DoesNotExist):
        error = "This note doesn't have this body"
        context = {
            "note": note,
            "error_message": error
        }
        return render(request, "notes/edit.html", context)
    return render(request, 'notes:post', context)

def post(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    body = get_object_or_404(Body, pk=request.GET["id"])
    try: 
        body.body_text = request.POST["body_text"]
        body.save()
    except (KeyError, Note.DoesNotExist):
        context = {
            "note": note,
            "error_message": "Essa nota não existe"
        }
        # return render(request, "notes/edit.html", context)
    context = { "note": note, "body": body }
    return render(request, "notes/post.html", context)

def vote(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    try: 
        selected_body = note.body_set.get(pk=request.POST["body"])
    except (KeyError, Note.DoesNotExist):
        return render(
            request,
            "notes/detail.html",
            {
                "note": note,
                "error_message": "You didn't select a choice"
            },
        ) 
    else: 
        selected_body.upvotes += 1
        selected_body.save()

    return HttpResponseRedirect(reverse("notes:body", args=((note.id,))))