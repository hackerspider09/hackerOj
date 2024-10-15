# Generated by Django 4.2.2 on 2024-08-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_registrationopen'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionServers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50, unique=True)),
                ('port', models.CharField(max_length=10)),
            ],
        ),
    ]
