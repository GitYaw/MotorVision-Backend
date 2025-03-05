from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.printHelloWorld),
    path("something/", views.printSomething),
    path("connect/", views.connect),
    path("start/", views.start),
    path("stop/", views.stop),
    path("", views.home_page)
]