# Generated by Django 2.1.4 on 2019-02-02 13:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20190202_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_message',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
