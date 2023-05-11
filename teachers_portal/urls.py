from django.urls import path
from . import views, views_client, views_miscelleneous
from django.views.generic import TemplateView
from . import views

app_name = "tp"
 
urlpatterns = [

    path("", views.index, name="index"),  

]