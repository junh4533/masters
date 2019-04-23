# Generated by Django 2.2 on 2019-04-19 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('assistant', 'Assistant')], max_length=9),
        ),
    ]