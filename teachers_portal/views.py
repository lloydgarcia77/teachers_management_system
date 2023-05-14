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
from django.contrib import messages

# NOTE: Email Activation 
from teachers_portal.tokens import account_activation_token  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.html import strip_tags
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.templatetags.static import static

from teachers_portal import forms, models, c_decorators
 
def login_page(request):
    template_name = "registration/login.html"  
    # NOTE: Redirects to the index page when trying to go back 
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("tp:index_page"))
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
      
        user = authenticate(email=email, password=password)
        if user:  
            if user.is_active and user.is_valid: 
                login(request, user) 
                # request.session.set_expiry(request.session.get_expiry_age())
                previous_page = request.GET.get('next', reverse("tp:index_page"))
                return HttpResponseRedirect(previous_page)
            else:
                messages.error(request, "Your account is needs approval, Please contact your administrator!")
        else:
            messages.error(request, "Your account is INVALID!")
        
    return render(request, template_name)


def user_pre_registration_page(request):
    template_name = "registration/register.html"
    
    if request.method == 'GET':
        form = forms.UserPreRegistrationForm(request.GET or None)
    elif request.method == 'POST':
        form = forms.UserPreRegistrationForm(request.POST or None)  
        if form.is_valid():
            userRegForm = form.save(commit=False)
            userRegForm.is_active = False
            userRegForm.is_staff = False
            userRegForm.is_superuser = False
            userRegForm.save() 
            
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email address'  
            to_email = form.cleaned_data.get('email') 

            html_message = render_to_string('registration/acc_active_email.html', {   
                'user': to_email,
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(userRegForm.pk)),  
                'token':account_activation_token.make_token(userRegForm),  
            })
 
            email = EmailMessage(  
                mail_subject, 
                html_message, 
                to=[to_email], 
            )  
            email.content_subtype = 'html'  
            email.send()  
            messages.success(request, "You have successfully registered, \
                please try to login when the Administrator approve/validated your account or  \
                you may check your E-mail for activation link.")
            return HttpResponseRedirect(reverse("login"))

    context = {
        'form': form,
    }

    return render(request, template_name, context)

@login_required
def user_post_registration_page(request):
    template_name = "registration/post_registration.html"
    user = request.user
    
    if hasattr(user,'fk_profile_detail_account'):
        return HttpResponseRedirect(reverse('tp:index_page'))

    if request.method == 'GET':
        form = forms.ProfileDetailForm(request.GET or None)
    elif request.method == 'POST':
        form = forms.ProfileDetailForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.account = user
            instance.save()

            messages.success(request,"Profile has been created successfully!")

            return HttpResponseRedirect(reverse('tp:index_page'))


    context = { 
        'form': form,
    }

    return render(request, template_name, context)



def activate(request, uidb64, token):
    template_name = 'registration/acc_activation_complete.html'  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  

    status = False
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True  
        user.is_valid = True  
        user.is_staff = False  
        user.is_superuser = False 
        user.save()  
        status = True

    context = {
        'status' : status
    }

    return render(request, template_name, context)
 
@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def index(request, *args, **kwargs):
    template_name = 'index.html'  
 
   
    context = {
        
    }
    return render(request, template_name, context)


@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def profile(request, *args, **kwargs):
    template_name = 'profile.html'  
    user = kwargs.get('user')

    profile = get_object_or_404(models.ProfileDetail, account=user) 
    if request.method == 'GET':
        form = forms.ProfileDetailForm(request.GET or None, instance=profile)
    elif request.method == 'POST':
        form = forms.ProfileDetailForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.save()

            messages.success(request,"Profile has been created successfully!")

            return HttpResponseRedirect(reverse('tp:index_page'))


    context = { 
        'form': form,
        'profile': profile,
    }
   
     
    return render(request, template_name, context)


@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def users_management(request, *args, **kwargs):
    template_name = 'users/users.html'  
    user = kwargs.get('user')

    users = models.User.objects.all()
 

    context = {  
        'profile': profile,
        'users': users,
        'user': user,
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def view_user(request, *args, **kwargs):
    template_name = 'users/view.html'  
     
    id = kwargs.get('id')
    user = get_object_or_404(models.User, id=id)
    profile = get_object_or_404(models.ProfileDetail, account=user)

    context = {  
        'profile': profile, 
        'user': user,
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def delete_user(request, *args, **kwargs):
    template_name = 'users/delete.html'  
    user = kwargs.get('user')

    id = kwargs.get('id')
    user = get_object_or_404(models.User, id=id) 

    if request.method == 'POST':
        user.delete()
        messages.success(request, "User has been deleted successfully!")
        
        return HttpResponseRedirect(reverse('tp:users_management'))

    context = {  
        'profile': profile, 
        'user': user,
    }
   
     
    return render(request, template_name, context)



@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def payroll_management(request, *args, **kwargs):
    template_name = 'payroll/payroll.html'  
    user = kwargs.get('user')
    
    payrolls = models.PayrollDetail.objects.all().order_by('-date_created')

    context = {  
        'profile': profile,
        'payrolls': payrolls,
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def create_payroll(request, *args, **kwargs):
    template_name = 'payroll/create.html'  
    user = kwargs.get('user')

    if request.method == 'GET':
        form = forms.PayrollDetailForm(request.GET or None)
    elif request.method == 'POST':
        form = forms.PayrollDetailForm(request.POST or None)
        if form.is_valid():
            form.save()

            messages.success(request, "Payroll successfully created")
            return HttpResponseRedirect(reverse('tp:payroll_management'))
 

    context = {  
        'profile': profile,
        'form': form,
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def edit_payroll(request, *args, **kwargs):
    template_name = 'payroll/edit.html'  
    user = kwargs.get('user')
    id = kwargs.get('id')
    payroll = get_object_or_404(models.PayrollDetail, id=id)
    if request.method == 'GET':
        form = forms.PayrollDetailForm(request.GET or None, instance=payroll)
    elif request.method == 'POST':
        form = forms.PayrollDetailForm(request.POST or None, instance=payroll)
        if form.is_valid():
            form.save()

            messages.info(request, "Payroll successfully updated")
            return HttpResponseRedirect(reverse('tp:payroll_management'))
 

    context = {  
        'profile': profile,
        'form': form,
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def print_payroll(request, *args, **kwargs):
    template_name = 'payroll/print.html'  
    user = kwargs.get('user')
    id = kwargs.get('id')
    payroll = get_object_or_404(models.PayrollDetail, id=id)
     

    context = {  
        'payroll': payroll, 
    }
   
     
    return render(request, template_name, context)

@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def delete_payroll(request, *args, **kwargs):
    template_name = 'payroll/delete.html'  
    user = kwargs.get('user')
    id = kwargs.get('id')
    payroll = get_object_or_404(models.PayrollDetail, id=id)
     
    if request.method == 'POST':
        payroll.delete()
        messages.success(request, f'{payroll.employee.get_full_name()}\'s spayroll has been deleted')

        return HttpResponseRedirect(reverse('tp:payroll_management'))
    context = {  
        'payroll': payroll, 
    }
   
     
    return render(request, template_name, context)



@login_required 
@c_decorators.is_authorized_user  
@c_decorators.has_profile  
def evalutaions_management(request, *args, **kwargs):
    template_name = 'profile.html'  
    user = kwargs.get('user')
 

    context = {  
        'profile': profile,
    }
   
     
    return render(request, template_name, context)


