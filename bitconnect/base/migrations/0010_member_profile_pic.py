# Generated by Django 2.1.4 on 2019-02-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_member_last_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(blank=True, height_field=240, null=True, upload_to='profile_pics', width_field=240),
        ),
    ]