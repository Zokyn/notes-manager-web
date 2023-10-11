from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 

app_name = "notes"
urlpatterns = [
    path("", views.NoteListView.as_view(), name="index"),
    path("<int:note_id>/", views.note, name="note"),
    path("<int:note_id>/new/", views.new, name="new"),
    path("<int:note_id>/edit/<int:body_id>", views.edit, name="edit"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
