# Generated by Django 4.1.4 on 2022-12-19 16:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_alter_doctor_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
