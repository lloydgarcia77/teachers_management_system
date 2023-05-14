# Generated by Django 3.2.14 on 2023-05-14 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_portal', '0010_evaluationform'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationform',
            name='comments_suggestions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluationform',
            name='td_q7',
            field=models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('execellent', 'execellent')], default='poor', max_length=50, verbose_name='Respects the data privacy and confidentiality of pertinent information gathered from the students.'),
        ),
    ]