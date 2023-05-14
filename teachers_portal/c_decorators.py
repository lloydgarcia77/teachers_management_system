from functools import wraps
from django.shortcuts import get_object_or_404
from django.urls import reverse
from teachers_portal import models
from django.http import HttpResponse, HttpResponseRedirect, Http404



def has_profile(view_function):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  
        

        if not hasattr(user,'fk_profile_detail_account'):
            return HttpResponseRedirect(reverse('user_post_registration_page'))
      
         
         
        kwargs['user'] = user
        return view_function(request, *args, **kwargs)
    return _wrapped_view

def is_authorized_user(view_function):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  
        

        if not (user.is_active and user.is_valid):
            raise Http404()
      
         
         
        kwargs['user'] = user
        return view_function(request, *args, **kwargs)
    return _wrapped_view