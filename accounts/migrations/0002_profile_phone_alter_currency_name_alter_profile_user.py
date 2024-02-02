# Generated by Django 4.2.9 on 2024-02-01 07:18

import accounts.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=3, validators=[accounts.utils.validation_currency]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
