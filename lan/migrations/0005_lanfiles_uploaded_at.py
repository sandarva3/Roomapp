# Generated by Django 5.0.6 on 2024-06-17 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0004_alter_lanfiles_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='lanfiles',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
