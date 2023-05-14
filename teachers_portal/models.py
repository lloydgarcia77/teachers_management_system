from django.conf import settings
from django.db import models
from django.db.models.base import Model
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import os, uuid, base64


def get_short_uuid(existing_uuid):
    # Convert the existing UUID to bytes
    uuid_bytes = existing_uuid.bytes

    # Encode the bytes using base64
    encoded_uuid = base64.urlsafe_b64encode(uuid_bytes)

    # Convert the encoded UUID back to a string
    short_uuid = encoded_uuid.decode('utf-8').rstrip('=')

    return short_uuid

class UserManager(BaseUserManager):
    """Manger for user profiles"""

    def create_user(self, email, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        """Create and save a new superuser with the given details"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customized model for user in django"""

 
    email = models.EmailField(max_length=50, unique=True)  
    date_added = models.DateTimeField(auto_now=True) 
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are  

    def __str__(self):
        return self.email
      
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
   
      

class ProfileDetail(models.Model): 
    # NOTE: NOTE: Model for profile details
    GENDER_LIST = (
        ('Male','Male'),
        ('Female','Female'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fk_profile_detail_account")  
    image = models.ImageField(upload_to="images/", blank=True,) 
    s_name = models.CharField(max_length=20, blank=True)
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    m_name = models.CharField(max_length=50, verbose_name="Middle Name", blank=True, null=True)
    l_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender = models.CharField(max_length=50, choices=GENDER_LIST, default='Male')
    dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField()

    position = models.CharField(max_length=150)
    # educ_background = models.TextField()
    highest_deg_attain = models.CharField(max_length=150, blank=True, null=True)
    course = models.CharField(max_length=150)
    school_grad = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    subject_coordinator = models.CharField(max_length=150)

    contact_no = models.CharField(max_length=15, verbose_name="Contact No", blank=True, null=True, unique=True, validators=[MinLengthValidator(10)]) 
  
    date_hired = models.DateTimeField(auto_now=True) 
 
    def get_full_name(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'

    def get_full_name_with_suffix(self):
        return f'{self.s_name} {self.f_name} {self.m_name} {self.l_name}'
    
    def get_short_name(self):
        return f'{self.f_name} {self.l_name}'
    
    def __str__(self):
        return self.get_full_name()
   
   
    def short_uuid(self):
        return get_short_uuid(self.id)
          
 
    def delete(self,*args,**kwargs):

        if self.image:
            if os.path.isfile(self.image.path) and os.path.exists(self.image.path):
                os.remove(self.e_signatimageure.path) 
        if self.e_signature:
            if os.path.isfile(self.e_signature.path) and os.path.exists(self.e_signature.path): 
                os.remove(self.e_signature.path) 
        super(ProfileDetail, self).delete(*args,**kwargs)
 


class PayrollDetail(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    employee = models.ForeignKey(ProfileDetail, on_delete=models.CASCADE, related_name="fk_payroll_detail_employee")  
    period_covered_from = models.DateField()
    period_covered_to = models.DateField()

    # NOTE: Total basic salary
    basic_ed = models.FloatField(null=True, default=0.0)
    college = models.FloatField(null=True, default=0.0)

    # NOTE: Add
    overload = models.FloatField(null=True, default=0.0)
    substitution = models.FloatField(null=True, default=0.0)
    overtime = models.FloatField(null=True, default=0.0)
    holiday_pay = models.FloatField(null=True, default=0.0)
    ndp = models.FloatField(null=True, default=0.0)
    honorarium = models.FloatField(null=True, default=0.0)
    longetivity = models.FloatField(null=True, default=0.0)
    merit_incetive_pay = models.FloatField(null=True, default=0.0)
    adj = models.FloatField(null=True, default=0.0)

    # NOTE: Allowances
    rice = models.FloatField(null=True, default=0.0)
    laundry = models.FloatField(null=True, default=0.0)
    uniform = models.FloatField(null=True, default=0.0)
    position = models.FloatField(null=True, default=0.0)

    # NOTE: Less
    absences = models.FloatField(null=True, default=0.0)
    tardiness_undertime = models.FloatField(null=True, default=0.0)
    sss_prem = models.FloatField(null=True, default=0.0)
    sss_loan = models.FloatField(null=True, default=0.0)

    pag_ibig_prem = models.FloatField(null=True, default=0.0)
    pag_ibig_loan = models.FloatField(null=True, default=0.0)
    philhealt_prem = models.FloatField(null=True, default=0.0) 
    withholding_tax = models.FloatField(null=True, default=0.0)

    landbank = models.FloatField(null=True, default=0.0)
    damayan = models.FloatField(null=True, default=0.0)
    salary_deductions = models.FloatField(null=True, default=0.0)
    uniform = models.FloatField(null=True, default=0.0)

    salary_loan = models.FloatField(null=True, default=0.0)
    tuition_fee = models.FloatField(null=True, default=0.0)
    snpl = models.FloatField(null=True, default=0.0)
    lbp_adj = models.FloatField(null=True, default=0.0)

    date_updated = models.DateTimeField(auto_now=True) 
    date_created = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.employee.get_full_name()

    def gross_pay(self):
        return sum([
            self.basic_ed,
            self.college,
            # NOTE: Add
            self.overload,
            self.substitution,
            self.overtime,
            self.holiday_pay,
            self.ndp,
            self.honorarium,
            self.longetivity,
            self.merit_incetive_pay,
            self.adj,
            # NOTE: Allowances
            self.rice,
            self.laundry,
            self.uniform,
            self.position,
        ])
 
    def net_pay(self):
        return self.gross_pay() - sum([
            self.absences,
            self.tardiness_undertime, 
            self.sss_prem,
            self.sss_loan,

            self.pag_ibig_prem,
            self.pag_ibig_loan,
            self.philhealt_prem,
            self.withholding_tax,

            self.landbank,
            self.salary_deductions,
            self.uniform,

            self.salary_loan,
            self.tuition_fee,
            self.snpl,
            self.lbp_adj ,
        ])
 

    def short_uuid(self):
        return get_short_uuid(self.id)


class EvaluationForm(models.Model): 
    RATINGS = (
        ('poor', 'poor'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('execellent', 'execellent'),
    )

    GENDER_LIST = (
        ('Male','Male'),
        ('Female','Female'),
    )
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    employee = models.ForeignKey(ProfileDetail, on_delete=models.CASCADE, related_name="fk_evaluation_employee")  

    name = models.CharField(max_length=250)
    course_year_sec = models.CharField(max_length=250)
    age = models.IntegerField()
    gender = models.CharField(max_length=15, choices=GENDER_LIST, default='Male')

    # NOTE: PLANNING AND PREPARATION

    pp_q1 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Distributes to students Outcomes-Based Education Teaching Learning (OBTL) syllabus at the beginning of the semester or quarter')
    pp_q2 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Explains the alignment of FCPC vision, mission, program educational objectives, program outcomes and course learning outcomes.')
    pp_q3 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Meets class on scheduled day and time.')

    # NOTE: TEACHING COMPETENCIES
    tc_q1 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Provides mastery of essential learning competencies of the course at the beginning of the class.')
    tc_q2 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Articulates objectives and purpose of the lesson and related course learning outcomes.')
    tc_q3 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Integrates FCPC core values in teaching the lessons.')
    tc_q4 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Encourages students to understand and actualize FCPC core values in applying the learned knowledge and skills of the lessons.')
    tc_q5 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Conducts interactive learning wherein the students participate actively in the learning activities.')
    tc_q6 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Provides appropriate variety, interesting, challenging, and effective learning activities to attain the objectives of each lesson. ')
    tc_q7 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Asks relevant and thought-provoking questions.')
    tc_q8 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Sustains student’s interest throughout the period while maintaining a safe and  healthy online environment. ')
    tc_q9 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Establishes clear connection between the lesson taught and the real world. Encourages the integration lessons to practical application to life. ')
    tc_q10 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Shows mastery of the subject matter.')
    tc_q11 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Responds to the students’ queries or needs appropriately both online and offline.')
    tc_q12 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Demonstrates fluency in English/Filipino as medium of instruction.')
    tc_q13 = models.CharField(max_length=50, choices=RATINGS, default='poor', verbose_name='Provides appropriate oral and written formative assessments for mastery of the knowledge and skills of the lessons')
    tc_q14 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Provides students needed support during and after the class instruction for them to gain mastery of the learning competencies.')
    tc_q15 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Gives grades to students based on their academic performance and learning assessments.')
    # NOTE: TEACHER’S DECORUM
    td_q1 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Shows professionalism in handling classroom instruction. ')
    td_q2 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Exhibits confidence, spontaneity and naturalness.')
    td_q3 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Uses appropriate language/correct vocabulary.')
    td_q4 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Gives clear/ precise instructions.')
    td_q5 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Demonstrates care, acceptance and respect for each student.')
    td_q6 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Provides guidance and assistance for referral in case of other needs of the students.')
    td_q7 = models.CharField(max_length=50, choices=RATINGS, default='poor',verbose_name='Respects the data privacy and confidentiality of pertinent information gathered from the students.')

    comments_suggestions = models.TextField(blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True) 

    
    def __str__(self):
        return self.employee.get_full_name()

    def get_ratings(self):
        RATING_MAP = {
            'poor': 1,
            'fair': 2,
            'good': 3,
            'execellent': 4,
        }


        rating_list = [
            RATING_MAP.get(self.pp_q1, 0),
            RATING_MAP.get(self.pp_q2, 0),
            RATING_MAP.get(self.pp_q3, 0),

            RATING_MAP.get(self.tc_q1, 0),
            RATING_MAP.get(self.tc_q2, 0),
            RATING_MAP.get(self.tc_q3, 0),
            RATING_MAP.get(self.tc_q4, 0),
            RATING_MAP.get(self.tc_q5, 0),
            RATING_MAP.get(self.tc_q6, 0),
            RATING_MAP.get(self.tc_q7, 0),
            RATING_MAP.get(self.tc_q8, 0),
            RATING_MAP.get(self.tc_q9, 0),
            RATING_MAP.get(self.tc_q10, 0),
            RATING_MAP.get(self.tc_q11, 0),
            RATING_MAP.get(self.tc_q12, 0),
            RATING_MAP.get(self.tc_q13, 0),
            RATING_MAP.get(self.tc_q14, 0),
            RATING_MAP.get(self.tc_q15, 0),

            RATING_MAP.get(self.td_q1, 0),
            RATING_MAP.get(self.td_q2, 0),
            RATING_MAP.get(self.td_q3, 0),
            RATING_MAP.get(self.td_q4, 0),
            RATING_MAP.get(self.td_q5, 0),
            RATING_MAP.get(self.td_q6, 0),
            RATING_MAP.get(self.td_q7, 0),
        ]

        print(sum(rating_list))
        return sum(rating_list) / len(rating_list)
