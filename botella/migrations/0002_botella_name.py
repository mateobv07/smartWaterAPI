# Generated by Django 4.1.3 on 2022-11-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botella', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botella',
            name='name',
            field=models.CharField(default='Name', max_length=30),
        ),
    ]