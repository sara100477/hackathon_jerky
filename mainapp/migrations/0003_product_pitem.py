# Generated by Django 2.2.3 on 2019-07-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20190725_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Pitem',
            field=models.CharField(max_length=20, null=True),
        ),
    ]