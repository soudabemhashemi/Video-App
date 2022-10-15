# Generated by Django 3.2.5 on 2021-09-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_alter_video_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.IntegerField(choices=[(1, 'هرزنامه ها'), (3, 'محتوای جنسی'), (5, 'اعمال مضر یا خطرناک'), (6, 'کودک آزاری'), (7, 'تروریسم را ترویج می دهد'), (13, 'False information'), (15, 'نقض مالکیت معنوی'), (18, 'توهین به قومیت ها یا نژادپرستی'), (20, 'Contrast the title and description with the content of the video.'), (22, 'سایر')]),
        ),
    ]
