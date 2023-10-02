from django.urls import path
from . import views 

app_name = "notes"
urlpatterns = [
    path("", views.NoteListView.as_view(), name="index"),
    path("<int:note_id>/", views.note, name="note"),
    path("<int:note_id>/new/", views.new, name="new"),
    path("<int:note_id>/post/", views.post, name="post"),
    path("<int:note_id>/edit/<int:body_id>", views.edit, name="edit"),
]
