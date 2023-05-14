from django.urls import path 
from django.views.generic import TemplateView
from . import views

app_name = "tp"
 
urlpatterns = [

    path("", views.index, name="index_page"),  
    path("profile/", views.profile, name="profile"),  
    path("users/", views.users_management, name="users_management"),  
    path("users/view/<int:id>/", views.view_user, name="view_user"),  
    path("users/delete/<int:id>/", views.delete_user, name="delete_user"),  

    path("payroll/", views.payroll_management, name="payroll_management"),  
    path("payroll/create/", views.create_payroll, name="create_payroll"),  
    path("payroll/edit/<uuid:id>/", views.edit_payroll, name="edit_payroll"),  
    path("payroll/print/<uuid:id>/", views.print_payroll, name="print_payroll"),  
    path("payroll/delete/<uuid:id>/", views.delete_payroll, name="delete_payroll"),  


    path("evaluations/", views.evalutaions_management, name="evalutaions_management"),  

]