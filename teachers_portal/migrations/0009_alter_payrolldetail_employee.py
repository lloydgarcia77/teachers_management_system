# Generated by Django 3.2.14 on 2023-05-14 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_portal', '0008_payrolldetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrolldetail',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_payroll_detail_employee', to='teachers_portal.profiledetail'),
        ),
    ]
