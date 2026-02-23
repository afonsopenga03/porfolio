from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("sobre", views.sobre, name="sobre"),
    path("skills", views.skills, name="skills"),
    path("contato", views.contato, name="contato"),
    path("projetos", views.projetos, name="projetos"),
    path("dashboard", views.dashboard, name="dashboard"),
     path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]