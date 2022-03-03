# Generated by Django 3.2 on 2022-03-02 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, primary_key=True, serialize=False, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('user_type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_super_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('email', 'user_type'), name='unique user'),
        ),
    ]
