# Generated by Django 4.1.1 on 2022-12-13 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IProductive', '0006_remove_profile_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userDays', to=settings.AUTH_USER_MODEL),
        ),
    ]
