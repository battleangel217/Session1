# Generated by Django 5.2.3 on 2025-07-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_remove_room_submitted_player_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='done_voting',
            field=models.BooleanField(default=False),
        ),
    ]
