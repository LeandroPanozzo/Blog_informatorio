# Generated by Django 5.1.1 on 2024-10-06 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Spa', '0002_denuncia'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='post_images'),
        ),
    ]