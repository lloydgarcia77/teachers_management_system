from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from . import models  

 
User = get_user_model()


class UserAdminCreationForms(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        '''
            Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match!")

        return self.cleaned_data

    def save(self, commit=True):
        """
            Save the provided password in hashed format
        """

        # Invoke the super class save funtion to trigger the save method
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class UserAdminChangeForm(forms.ModelForm):
    """
        A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class UserPreRegistrationForm(forms.ModelForm): 
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirm', widget=forms.PasswordInput) 
    class Meta:
        model = User
        exclude = ('date_added', 'is_active', 'is_staff',
                   'is_superuser', 'password')

    def __init__(self, *args, **kwargs):
        super(UserPreRegistrationForm, self).__init__(*args, **kwargs)
        """
            Apply predefined attributes of html element
        """

        self.fields['email'].widget.attrs = {
            'class': 'form-control secret-input',
            'placeholder': 'E-Mail',
            'required': 'required'
        }
 

        self.fields['password1'].widget.attrs = {
            'type': 'text',
            'class': 'form-control secret-input password',
            'placeholder': 'Password',
        }

        self.fields['password2'].widget.attrs = {
            'type': 'text',
            'class': 'form-control secret-input password',
            'placeholder': 'Confirm Password',
        }

    def clean_email(self):
        """
            Validates the integrity of email
        """

        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("E-mail is already taken.")
        return email

    def clean_password2(self): 

        MIN_LEN = 6
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']

        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                   '*', '(', ')', '<', '!']

        WITH_DIGITS = False
        WITH_LCASE_CHARS = False
        WITH_UCASE_CHARS = False
        WITH_SYMBOLS = False
        WITH_REPEATABLE_CHARS = False

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1) < MIN_LEN and len(password2) < MIN_LEN:
            raise forms.ValidationError("Password is too short!")
        else:
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            # else:
            #     for d in DIGITS:
            #         if d in password2:
            #             WITH_DIGITS = True
            #             break

            #     for lc in LOCASE_CHARACTERS:
            #         if lc in password2:
            #             WITH_LCASE_CHARS = True
            #             break
            #     for uc in UPCASE_CHARACTERS:
            #         if uc in password2:
            #             WITH_UCASE_CHARS = True
            #             break
            #     for s in SYMBOLS:
            #         if s in password2:
            #             WITH_SYMBOLS = True
            #             break

            #     for c in range(len(password2)):
            #         index = c + 1
            #         if index < len(password2):
            #             if password2[c] == password2[c+1]:
            #                 WITH_REPEATABLE_CHARS = True

            #     if not (WITH_DIGITS and WITH_SYMBOLS and WITH_UCASE_CHARS and WITH_LCASE_CHARS and not WITH_REPEATABLE_CHARS):
            #         raise forms.ValidationError(
            #             "Your password is too weak, please include characters with Uppercases, Lowercases, Special characters, and dont include repeated characters!")

        return password2

    def save(self, commit=True):
        user = super(UserPreRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user



class ProfileDetailForm(forms.ModelForm):

   

    def __init__(self, *args, **kwargs):
        super(ProfileDetailForm, self).__init__(*args, **kwargs)
 
        self.fields['s_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Suffix Name',
        }

        self.fields['f_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'required'
        }

        self.fields['m_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Middle Name',
            'required': 'required'
        }

        self.fields['l_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'required'
        }

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'form-control select2',
            'style': 'width: 100%',
        }

        self.fields['age'].widget.attrs = {
            'type': 'number',
            'class': 'form-control',
            'max': '100',
            'min': '1',
        }

        self.fields['contact_no'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Contact No', 
            'required': 'required', 
        }
 

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'form-control select2',
            'style': 'width: 100%',
        }

        self.fields['address'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }

        self.fields['position'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 
 
 
        self.fields['highest_deg_attain'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 
 
        self.fields['course'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 
 
        self.fields['school_grad'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 
 
        self.fields['department'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 
 
        self.fields['subject_coordinator'].widget.attrs = {
            'type': 'text',
            'class': 'form-control', 
        }
 

    class Meta:
        model = models.ProfileDetail
        exclude = ('id', 'account', 'date_hired',)
        widgets = {
            'dob': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }



class PayrollDetailForm(forms.ModelForm):

    class Meta:
        model = models.PayrollDetail
        exclude = ('id', 'date_updated', 'date_created',)
        widgets = {
            'period_covered_from': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'period_covered_to': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


   

    def __init__(self, *args, **kwargs):
        super(PayrollDetailForm, self).__init__(*args, **kwargs)
 
        self.fields['employee'].widget.attrs = {
            'class': 'form-control', 
        }
 
        self.fields['basic_ed'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['college'].widget.attrs = {
            'class': 'form-control', 
        }

        self.fields['overload'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['substitution'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['overtime'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['holiday_pay'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['ndp'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['honorarium'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['longetivity'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['merit_incetive_pay'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['adj'].widget.attrs = {
            'class': 'form-control', 
        }

        self.fields['rice'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['laundry'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['uniform'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['position'].widget.attrs = {
            'class': 'form-control', 
        }

        self.fields['absences'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['tardiness_undertime'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['sss_prem'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['sss_loan'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['pag_ibig_prem'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['pag_ibig_loan'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['philhealt_prem'].widget.attrs = {
            'class': 'form-control', 
        }

        self.fields['withholding_tax'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['landbank'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['damayan'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['salary_deductions'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['uniform'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['salary_loan'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['tuition_fee'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['snpl'].widget.attrs = {
            'class': 'form-control', 
        }
        self.fields['lbp_adj'].widget.attrs = {
            'class': 'form-control', 
        }