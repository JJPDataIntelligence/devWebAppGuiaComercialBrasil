# Generated by Django 2.1.5 on 2019-09-10 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0005_auto_20190909_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidade',
            name='latitude',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='cidade',
            name='longitude',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='latitude',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='longitude',
            field=models.CharField(max_length=10),
        ),
    ]
