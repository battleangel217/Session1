# Generated by Django 5.2.3 on 2025-06-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_rename_student_studentsenrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsenrolled',
            name='age',
            field=models.IntegerField(default=17),
        ),
    ]
