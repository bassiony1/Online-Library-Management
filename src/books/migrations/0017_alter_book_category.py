# Generated by Django 3.2.7 on 2021-09-20 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_alter_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='books.Category'),
        ),
    ]