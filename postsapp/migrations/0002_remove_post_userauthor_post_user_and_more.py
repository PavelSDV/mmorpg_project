# Generated by Django 4.2.1 on 2023-06-07 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import postsapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postsapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='userAuthor',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentFile',
            field=models.FileField(upload_to='files'),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentImage',
            field=models.ImageField(upload_to=postsapp.models.user_directory_path),
        ),
    ]