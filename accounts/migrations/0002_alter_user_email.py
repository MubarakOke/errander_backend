# Generated by Django 3.2 on 2022-03-19 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='email address'),
        ),
    ]
