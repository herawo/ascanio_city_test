# Generated by Django 3.0.8 on 2020-08-01 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city_app', '0003_auto_20200801_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='zip_codes',
        ),
        migrations.AddField(
            model_name='city',
            name='zip_code',
            field=models.CharField(default="None", max_length=10),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ZipCode',
        ),
    ]
