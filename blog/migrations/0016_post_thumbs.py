# Generated by Django 3.0.8 on 2022-07-04 12:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbs',
            field=models.ManyToManyField(blank=True, default='0', related_name='thumbs', to=settings.AUTH_USER_MODEL),
        ),
    ]
