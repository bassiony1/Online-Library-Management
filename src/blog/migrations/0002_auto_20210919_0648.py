# Generated by Django 3.2.7 on 2021-09-19 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='ow',
            new_name='author',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default_book.jpg', upload_to='blog_images'),
        ),
    ]
