# Generated by Django 3.0.8 on 2022-06-16 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]