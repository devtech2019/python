# Generated by Django 3.2 on 2022-04-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant_web', '0009_applicantdeatails_vaccination_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantdeatails',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vaccination'),
        ),
    ]
