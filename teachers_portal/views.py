from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import (
    JsonResponse,
    Http404,
    HttpResponseRedirect
)
from django.core.signing import Signer
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q, F
from django.db.utils import IntegrityError, DataError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required


# @login_required  
def index(request, *args, **kwargs):
    template_name = 'index.html'  


   
    context = {
        
    }
    return render(request, template_name, {})
