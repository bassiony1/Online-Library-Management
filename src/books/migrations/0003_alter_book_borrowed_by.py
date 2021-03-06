# Generated by Django 3.2.7 on 2021-09-09 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_alter_book_borrowed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='borrowed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_borrowing', to=settings.AUTH_USER_MODEL),
        ),
    ]
