from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("blog/<str:slug>/", views.blog, name='blog'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("<str:name>/", views.categories, name='categories'),
    path("login",views.login, name='login'),
    path("registration",views.registration, name='registration'),
    path("logout",views.logout, name='logout'),
]
