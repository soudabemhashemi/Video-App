# Generated by Django 3.2.5 on 2021-09-15 11:12

import django.core.validators
from django.db import migrations, models
import video.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_merge_0009_video_poster_0012_auto_20210914_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='video/posters/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), video.utils.validators.FileSizeValidator(max_size=512000)], verbose_name='Poster'),
        ),
    ]
