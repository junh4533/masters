# Generated by Django 2.2 on 2019-04-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_auto_20190419_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='picture',
            field=models.ImageField(blank=True, upload_to='patients'),
        ),
    ]