# Generated by Django 2.1.4 on 2019-02-02 13:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_messages_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]