from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader 
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
    return HttpResponse("You're liking a body %s note" % note_id)