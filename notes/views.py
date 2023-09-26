from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from .models import Note

# Create your views here.
def index(request):
    latest_note_list = Note.objects.order_by("-pub_date")[:10]
    context = {
        "latest_note_list": latest_note_list
    }
    return render(request, "notes/index.html", context)

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, "notes/detail.html", {"note": note})

def results(request, note_id):
    return HttpResponse("You're looking at a body %s" % note_id)

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