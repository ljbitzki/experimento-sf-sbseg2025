# Generated by Django 5.1.5 on 2025-05-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_sot_hostname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='hostname',
            field=models.CharField(default='172.18.0.5', max_length=80),
        ),
    ]
