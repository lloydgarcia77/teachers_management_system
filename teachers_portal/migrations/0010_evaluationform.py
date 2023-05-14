# Generated by Django 3.2.14 on 2023-05-14 16:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_portal', '0009_alter_payrolldetail_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationForm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('course_year_sec', models.CharField(max_length=250)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=15)),
                ('pp_q1', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Distributes to students Outcomes-Based Education Teaching Learning (OBTL) syllabus at the beginning of the semester or quarter')),
                ('pp_q2', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Explains the alignment of FCPC vision, mission, program educational objectives, program outcomes and course learning outcomes.')),
                ('pp_q3', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Meets class on scheduled day and time.')),
                ('tc_q1', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Provides mastery of essential learning competencies of the course at the beginning of the class.')),
                ('tc_q2', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Articulates objectives and purpose of the lesson and related course learning outcomes.')),
                ('tc_q3', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Integrates FCPC core values in teaching the lessons.')),
                ('tc_q4', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Encourages students to understand and actualize FCPC core values in applying the learned knowledge and skills of the lessons.')),
                ('tc_q5', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Conducts interactive learning wherein the students participate actively in the learning activities.')),
                ('tc_q6', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Provides appropriate variety, interesting, challenging, and effective learning activities to attain the objectives of each lesson. ')),
                ('tc_q7', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Asks relevant and thought-provoking questions.')),
                ('tc_q8', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Sustains student’s interest throughout the period while maintaining a safe and  healthy online environment. ')),
                ('tc_q9', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Establishes clear connection between the lesson taught and the real world. Encourages the integration lessons to practical application to life. ')),
                ('tc_q10', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Shows mastery of the subject matter.')),
                ('tc_q11', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Responds to the students’ queries or needs appropriately both online and offline.')),
                ('tc_q12', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Demonstrates fluency in English/Filipino as medium of instruction.')),
                ('tc_q13', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Provides appropriate oral and written formative assessments for mastery of the knowledge and skills of the lessons')),
                ('tc_q14', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Provides students needed support during and after the class instruction for them to gain mastery of the learning competencies.')),
                ('tc_q15', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Gives grades to students based on their academic performance and learning assessments.')),
                ('td_q1', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Shows professionalism in handling classroom instruction. ')),
                ('td_q2', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Exhibits confidence, spontaneity and naturalness.')),
                ('td_q3', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Uses appropriate language/correct vocabulary.')),
                ('td_q4', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Gives clear/ precise instructions.')),
                ('td_q5', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Demonstrates care, acceptance and respect for each student.')),
                ('td_q6', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Provides guidance and assistance for referral in case of other needs of the students.')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_evaluation_employee', to='teachers_portal.profiledetail')),
            ],
        ),
    ]