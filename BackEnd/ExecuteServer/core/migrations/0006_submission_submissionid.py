# Generated by Django 4.2.2 on 2024-08-09 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_submission_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submissionId',
            field=models.TextField(blank=True, null=True),
        ),
    ]
