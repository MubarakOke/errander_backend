# Generated by Django 3.2 on 2022-03-05 00:06

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.blog_image_location),
        ),
    ]
