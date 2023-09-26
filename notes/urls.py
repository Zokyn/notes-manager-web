from django.urls import path
from . import views 

app_name = "notes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:note_id>/", views.detail, name="note"),
    path("<int:note_id>/body/", views.results, name="body"),
    path("<int:note_id>/vote/", views.vote, name="vote")
]
