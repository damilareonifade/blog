# Generated by Django 3.0.8 on 2022-06-16 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_excerpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
