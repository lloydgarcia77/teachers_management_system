"""fcpc_teachers_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from teachers_portal import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('teachers_portal.urls')),

    
    #  NOTE: Login page
    path('login/', views.login_page, name="login"), 
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # NOTE: Registraion
    path('user-pre-registration/', views.user_pre_registration_page, name="user_pre_registration_page"),
    path('user-post-registration/', views.user_post_registration_page, name="user_post_registration_page"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 

    
    #  NOTE: Update password
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    
    # NOTE:  Password reset
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
