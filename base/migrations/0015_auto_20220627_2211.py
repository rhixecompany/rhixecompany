# Generated by Django 3.0.8 on 2022-06-27 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20220627_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
    ]
