# Generated by Django 3.2.5 on 2021-09-12 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_auto_20210911_0249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='video',
            name='playlist_order',
        ),
        migrations.AddField(
            model_name='playlist',
            name='privacy',
            field=models.CharField(choices=[('public', 'public'), ('unlisted', 'unlisted'), ('private', 'private')], default='public', max_length=8, verbose_name='privacy'),
        ),
        migrations.CreateModel(
            name='PlaylistVideoRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Added at')),
                ('order', models.PositiveIntegerField(verbose_name='Playlist order')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.playlist')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
            options={
                'unique_together': {('playlist', 'video'), ('playlist', 'order')},
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(related_name='playlists', through='video.PlaylistVideoRelation', to='video.Video', verbose_name='Videos'),
        ),
    ]
