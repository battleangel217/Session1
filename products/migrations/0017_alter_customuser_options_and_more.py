# Generated by Django 5.2.3 on 2025-07-05 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('email', 'username')},
        ),
    ]
