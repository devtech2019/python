# Generated by Django 3.2 on 2022-04-07 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicant_web', '0003_auto_20220407_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='applicant_review',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='approve_date',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='employee_review',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='sign_img',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='status',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='submit_status',
        ),
    ]
