# Generated by Django 2.1.5 on 2019-09-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0004_cidades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=2)),
                ('estado', models.CharField(max_length=2)),
                ('cidade', models.CharField(max_length=200)),
                ('bairro', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.CharField(max_length=5)),
                ('longitude', models.CharField(max_length=5)),
            ],
        ),
        migrations.DeleteModel(
            name='Cidades',
        ),
    ]
