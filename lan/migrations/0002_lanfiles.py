# Generated by Django 5.0.6 on 2024-06-12 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lanfiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(null=True, upload_to='C:\\Users\\Asus\\Desktop\\Room\\venv\\src\\lan/lanmedia')),
            ],
        ),
    ]
