# Generated by Django 3.2.5 on 2021-10-02 10:18

from django.db import migrations, models
import video.models.link


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0017_merge_0015_contactus_0016_alter_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='privacy',
            field=models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('UNLISTED', 'UNLISTED'), ('PRIVATE', 'PRIVATE')], default='PUBLIC', max_length=8, verbose_name='privacy'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.CharField(max_length=500, validators=[video.models.link.validate_url], verbose_name='Link'),
        ),
    ]
