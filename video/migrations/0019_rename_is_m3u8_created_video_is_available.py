# Generated by Django 3.2.5 on 2021-10-02 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0018_auto_20211002_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='is_m3u8_created',
            new_name='is_available',
        ),
    ]
