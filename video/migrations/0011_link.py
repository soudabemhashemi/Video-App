# Generated by Django 3.2.5 on 2021-09-14 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_delete_watchlater'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('link', models.URLField(verbose_name='Link')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='video.channel', verbose_name='Channel')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'unique_together': {('channel', 'link'), ('channel', 'title')},
            },
        ),
    ]
